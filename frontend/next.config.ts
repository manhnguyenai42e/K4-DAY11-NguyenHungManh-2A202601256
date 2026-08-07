import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  devIndicators: false,
  async rewrites() {
    return [
      {
        source: "/api/backend/:path*",
        destination: "http://localhost:14001/api/:path*",
      },
      {
        source: "/api/chat",
        destination: "http://localhost:14001/api/chat",
      },
      {
        source: "/api/chat/:path*",
        destination: "http://localhost:14001/api/chat/:path*",
      },
    ];
  },
};

export default nextConfig;