import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import { cleanSlug } from '../lib/slug';
import type { APIContext } from 'astro';

export async function GET(context: APIContext) {
  const posts = (await getCollection('posts', ({ data }) => !data.draft)).sort(
    (a, b) => b.data.published.getTime() - a.data.published.getTime(),
  );
  return rss({
    title: '… And Out Come the Systems – Writing',
    description: 'Complex systems, health and well-being amidst uncertainty.',
    site: context.site!,
    items: posts.map((e) => {
      const link = `/posts/${cleanSlug(e.id)}/`;
      // Use the original WP <guid> when available so existing RSS subscribers
      // (Feedly, Inoreader, etc.) do not re-receive the entire archive after
      // the Phase 3 DNS cutover. Falls back to canonical URL for placeholder
      // and native posts (which have no wp_guid set).
      // customData Object.assign-overwrites item.guid set from link — no duplicates.
      const guid = e.data.wp_guid ?? new URL(link, context.site!).toString();
      return {
        title: e.data.title,
        description: e.data.description,
        pubDate: e.data.published,
        link,
        customData: `<guid isPermaLink="false">${guid}</guid>`,
      };
    }),
  });
}
