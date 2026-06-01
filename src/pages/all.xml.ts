import rss from '@astrojs/rss';
import { allLive } from '../lib/collections';
import { cleanSlug } from '../lib/slug';
import { wpGuidCustomData } from '../lib/rss-guid';
import type { APIContext } from 'astro';

export async function GET(context: APIContext) {
  const items = await allLive();
  return rss({
    title: '… And Out Come the Systems – All writing',
    description: 'Complex systems, health and well-being amidst uncertainty.',
    site: context.site!,
    items: items.map((e) => {
      const link = `/${e.collection}/${cleanSlug(e.id)}/`;
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
