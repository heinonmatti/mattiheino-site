import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import { cleanSlug } from '../lib/slug';
import type { APIContext } from 'astro';

export async function GET(context: APIContext) {
  const items = (await getCollection('applied-musings', ({ data }) => !data.draft)).sort(
    (a, b) => b.data.published.getTime() - a.data.published.getTime(),
  );
  return rss({
    title: '… And Out Come the Systems – Applied musings',
    description: 'Behaviour change and thriving amidst uncertainty – light and practical.',
    site: context.site!,
    items: items.map((e) => {
      const link = `/applied-musings/${cleanSlug(e.id)}/`;
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
