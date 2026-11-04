import { plantPayload, plantRoute, searchPlantPapers } from "@/lib/plant-catalog";
export function POST(request: Request) { return plantRoute(request, async () => searchPlantPapers(await plantPayload(request))); }
