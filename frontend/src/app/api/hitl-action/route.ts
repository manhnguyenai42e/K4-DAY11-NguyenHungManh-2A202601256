import { NextRequest, NextResponse } from "next/server";

// Server-side proxy for HITL admin actions (approve/reject/custom reply).
//
// The browser never sees HITL_ADMIN_TOKEN — it lives only in this Node.js
// route handler (no NEXT_PUBLIC_ prefix, never bundled to client JS). The
// FastAPI backend at :14001 still checks X-Admin-Token itself; this route
// just keeps the secret out of the client bundle instead of shipping it
// via NEXT_PUBLIC_HITL_ADMIN_TOKEN.
const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:14001";
const ADMIN_TOKEN = process.env.HITL_ADMIN_TOKEN || "";

export async function POST(req: NextRequest) {
  if (!ADMIN_TOKEN) {
    return NextResponse.json(
      { error: "HITL_ADMIN_TOKEN chưa được cấu hình trên server Next.js (.env.local)." },
      { status: 503 }
    );
  }

  const body = await req.json();

  const res = await fetch(`${BACKEND_URL}/api/chat/action`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Admin-Token": ADMIN_TOKEN,
    },
    body: JSON.stringify(body),
  });

  const data = await res.json().catch(() => ({}));
  return NextResponse.json(data, { status: res.status });
}
