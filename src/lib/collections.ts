import { getCollection } from 'astro:content';

export type Collection = 'posts' | 'applied-musings';
export type Item = { collection: Collection; id: string; data: any };

const tag =
  (collection: Collection) =>
  (e: any): Item => ({ collection, id: e.id, data: e.data });

const byNewest = (a: Item, b: Item) =>
  b.data.published.getTime() - a.data.published.getTime();

export async function livePosts(): Promise<Item[]> {
  return (await getCollection('posts', ({ data }) => !data.draft)).map(tag('posts'));
}

export async function liveMusings(): Promise<Item[]> {
  return (await getCollection('applied-musings', ({ data }) => !data.draft)).map(
    tag('applied-musings'),
  );
}

export async function allLive(): Promise<Item[]> {
  return [...(await livePosts()), ...(await liveMusings())].sort(byNewest);
}

// Internal vetting backlog: anything still pending, drafts included, oldest first.
export async function pendingAll(): Promise<Item[]> {
  const p = (await getCollection('posts', ({ data }) => data.vetting_status === 'pending')).map(
    tag('posts'),
  );
  const m = (
    await getCollection('applied-musings', ({ data }) => data.vetting_status === 'pending')
  ).map(tag('applied-musings'));
  return [...p, ...m].sort((a, b) => a.data.published.getTime() - b.data.published.getTime());
}
