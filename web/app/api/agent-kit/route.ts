export function GET(request: Request) {
  return Response.redirect(new URL('/plantcell-agent-pipeline.zip',request.url),307);
}
