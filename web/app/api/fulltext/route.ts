import { plantRoute, readPlantFulltext } from "@/lib/plant-catalog";
export function GET(request: Request) { return plantRoute(request, () => readPlantFulltext(new URL(request.url).searchParams.get("pmid") ?? "")); }
