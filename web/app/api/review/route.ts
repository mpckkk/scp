import { plantPayload, plantRoute, reviewPlantPaper } from "@/lib/plant-catalog";
export function POST(request: Request) { return plantRoute(request, async (actor) => reviewPlantPaper(await plantPayload(request), actor)); }
