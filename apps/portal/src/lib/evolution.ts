import { env } from "@/lib/env";

export type EvolutionInstanceStatus = {
  instanceName: string;
  connected: boolean;
  phone?: string;
};

type EvolutionStatusResponse = {
  instance?: {
    instanceName?: string;
    state?: string;
    owner?: string;
  };
};

export class EvolutionClient {
  constructor(
    private readonly baseUrl = env.evolutionBaseUrl,
    private readonly apiKey = env.evolutionApiKey,
  ) {}

  async getInstanceStatus(instanceName: string): Promise<EvolutionInstanceStatus | null> {
    if (!this.baseUrl || !this.apiKey) {
      return null;
    }

    const response = await fetch(`${this.baseUrl}/instance/connectionState/${instanceName}`, {
      headers: {
        apikey: this.apiKey,
        "content-type": "application/json",
      },
      next: { revalidate: 30 },
    });

    if (!response.ok) {
      throw new Error("evolution_status_failed");
    }

    const body = (await response.json()) as EvolutionStatusResponse;
    return {
      instanceName: body.instance?.instanceName ?? instanceName,
      connected: body.instance?.state === "open",
      phone: body.instance?.owner,
    };
  }
}

export const evolution = new EvolutionClient();
