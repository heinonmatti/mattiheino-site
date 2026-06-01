import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import { cleanSlug } from '../lib/slug';
import { wpGuidCustomData } from '../lib/rss-guid';
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
      // See src/lib/rss-guid.ts for subscriber-continuity rationale.
      return {
        title: e.data.title,
        description: e.data.description,
        pubDate: e.data.published,
        link,
        customData: wpGuidCustomData(e.data.wp_guid, link, context.site!),
      };
    }),
  });
}
