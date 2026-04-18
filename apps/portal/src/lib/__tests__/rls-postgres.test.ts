import { randomUUID } from "node:crypto";
import { readFile } from "node:fs/promises";
import { join } from "node:path";
import { Client } from "pg";
import { describe, expect, it } from "vitest";

const databaseUrl = process.env.PORTAL_TEST_DATABASE_URL;

const describeWithDatabase = databaseUrl ? describe : describe.skip;

describeWithDatabase("portal RLS policies", () => {
  it("prevents a tenant A user from reading tenant B rows", async () => {
    const schema = `portal_test_${randomUUID().replaceAll("-", "_")}`;
    const userA = "00000000-0000-4000-8000-00000000000a";
    const userB = "00000000-0000-4000-8000-00000000000b";
    const client = new Client({ connectionString: databaseUrl });

    await client.connect();

    try {
      await client.query(`create schema ${schema}`);
      await client.query(`set search_path to ${schema}, public`);
      await client.query(`create extension if not exists pgcrypto`);
      await client.query(`create schema if not exists auth`);
      await client.query(`
        create table if not exists auth.users (
          id uuid primary key
        )
      `);
      await client.query(`
        create or replace function auth.uid()
        returns uuid
        language sql
        stable
        as $$
          select nullif(current_setting('request.jwt.claim.sub', true), '')::uuid
        $$;
      `);
      await client.query(`
        do $$
        begin
          if not exists (select 1 from pg_roles where rolname = 'authenticated') then
            create role authenticated;
          end if;
        end $$;
      `);

      const migration = await readFile(
        join(process.cwd(), "supabase", "migrations", "0001_portal_schema.sql"),
        "utf8",
      );
      await client.query(migration);

      await client.query(`grant usage on schema public to authenticated`);
      await client.query(`grant select on all tables in schema public to authenticated`);

      await client.query(`insert into auth.users (id) values ($1), ($2) on conflict do nothing`, [
        userA,
        userB,
      ]);
      await client.query(
        `insert into public.tenant_members (tenant_id, user_id, role) values
          ('tenant-a', $1, 'owner'),
          ('tenant-b', $2, 'owner')`,
        [userA, userB],
      );
      await client.query(
        `insert into public.portal_bookings (tenant_id, customer_name, starts_at, source, status) values
          ('tenant-a', 'Cliente A', now(), 'WhatsApp', 'Confirmado'),
          ('tenant-b', 'Cliente B', now(), 'WhatsApp', 'Confirmado')`,
      );

      await client.query("begin");
      await client.query("set local role authenticated");
      await client.query(`set local "request.jwt.claim.sub" = '${userA}'`);
      const result = await client.query<{ tenant_id: string; customer_name: string }>(
        "select tenant_id, customer_name from public.portal_bookings order by tenant_id",
      );
      await client.query("rollback");

      expect(result.rows).toEqual([{ tenant_id: "tenant-a", customer_name: "Cliente A" }]);
    } finally {
      await client.query(`drop schema if exists ${schema} cascade`);
      await client.end();
    }
  });
});
