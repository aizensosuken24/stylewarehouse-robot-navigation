export default function handler(req, res) {
  // Lightweight health endpoint to verify Vercel functions are working
  res.status(200).json({ ok: true, service: "stylewarehouse-robot-navigation" });
}
