export default function handler(req, res) {
  // Catch-all proxy for API routes to prevent invocation failures
  // Provides a safe JSON response instead of crashing when other functions fail.
  res.status(200).json({
    ok: false,
    message: "This API route is currently disabled for safety. Contact the owner to enable specific endpoints.",
    path: req.url,
  });
}
