import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import path from "path";

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  build: {
    outDir: "../supplier_portal/public",
    emptyOutDir: false,
    target: "es2015",
    cssCodeSplit: false,
    rollupOptions: {
      input: path.resolve(__dirname, "src/main.js"),
      output: {
        entryFileNames: "supplier_portal.bundle.js",
        assetFileNames: "supplier_portal.bundle.css",
        inlineDynamicImports: true,
      },
    },
  },
  server: {
    port: 8080,
    proxy: {
      "^/(api|login|app|assets)": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },
  optimizeDeps: {
    include: ["frappe-ui > feather-icons", "showdown", "engine.io-client"],
  },
});
