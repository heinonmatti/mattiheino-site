// Content files are named `YYYY-MM-DD-slug.md` for chronological repo listing,
// but URLs should be clean (`/posts/slug/`). Strip the leading date for routing.
export const cleanSlug = (id: string): string =>
  id.replace(/^\d{4}-\d{2}-\d{2}-/, '');
