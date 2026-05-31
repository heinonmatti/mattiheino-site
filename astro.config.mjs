// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  site: 'https://mattiheino.com',
  integrations: [
    sitemap({
      // Internal-only backlog page must never enter the sitemap.
      filter: (page) => !page.includes('/vetting-queue'),
    }),
  ],
});
