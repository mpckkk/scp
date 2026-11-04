import { exportPlantCsv, plantRoute } from "@/lib/plant-catalog";
import type { PaperStatus } from "@/lib/plant-validation";
export function GET(request: Request) {
  return plantRoute(request, async () => new Response(await exportPlantCsv((new URL(request.url).searchParams.get("status") ?? "include") as PaperStatus), {
    headers: { "Content-Type": "text/csv; charset=utf-8", "Content-Disposition": 'attachment; filename="plant_single_cell_catalog.csv"', "Cache-Control": "no-store" },
  }));
}
