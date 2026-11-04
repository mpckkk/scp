import { getPlantPaper, plantRoute } from "@/lib/plant-catalog";
export function GET(request: Request) { return plantRoute(request, async () => ({ paper: await getPlantPaper(new URL(request.url).searchParams.get("pmid") ?? "") })); }
