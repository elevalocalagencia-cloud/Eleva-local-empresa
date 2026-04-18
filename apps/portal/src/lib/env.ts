const optional = (key: string): string | undefined => {
  const value = process.env[key];
  return value && value.length > 0 ? value : undefined;
};

export const env = {
  appUrl: optional("NEXT_PUBLIC_APP_URL") ?? "http://localhost:3000",
  demoTenantId: optional("NEXT_PUBLIC_DEMO_TENANT_ID"),
  supabaseUrl: optional("NEXT_PUBLIC_SUPABASE_URL"),
  supabaseAnonKey: optional("NEXT_PUBLIC_SUPABASE_ANON_KEY"),
  supabaseServiceRoleKey: optional("SUPABASE_SERVICE_ROLE_KEY"),
  chatwootBaseUrl: optional("CHATWOOT_BASE_URL"),
  chatwootAccountId: optional("CHATWOOT_ACCOUNT_ID"),
  chatwootApiToken: optional("CHATWOOT_API_ACCESS_TOKEN"),
  chatwootInboxId: optional("CHATWOOT_INBOX_ID"),
  evolutionBaseUrl: optional("EVOLUTION_BASE_URL"),
  evolutionApiKey: optional("EVOLUTION_API_KEY"),
};
