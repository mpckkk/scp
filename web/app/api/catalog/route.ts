import { plantCatalog, plantRoute } from "@/lib/plant-catalog";
export function GET(request: Request) { return plantRoute(request, () => plantCatalog()); }
