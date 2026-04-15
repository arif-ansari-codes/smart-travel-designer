import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "media.tacdn.com",
      },
      {
        protocol: "https",
        hostname: "**.tripadvisor.com",
      },
    ],
  },
};

export default nextConfig;
