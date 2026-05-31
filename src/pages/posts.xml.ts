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
    items: posts.map((e) => ({
      title: e.data.title,
      description: e.data.description,
      pubDate: e.data.published,
      link: `/posts/${cleanSlug(e.id)}/`,
      // NOTE (Phase 3 cutover): the default <guid> is the NEW URL. Before the
      // WordPress DNS cutover we must instead emit each post's ORIGINAL WP
      // <guid> (captured from the export) so existing RSS subscribers are not
      // re-served the entire archive as "new".
    })),
  });
}
