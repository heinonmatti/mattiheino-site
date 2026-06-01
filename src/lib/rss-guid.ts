/**
 * Build the RSS <guid> customData string for an item.
 *
 * Uses wp_guid (the original WordPress <guid>) when set, falling back to the
 * canonical URL. Critical for Phase 3 DNS cutover — existing WP RSS subscribers
 * dedupe on <guid>, so emitting the original WP guid prevents the entire
 * archive being re-broadcast as new items.
 *
 * Verified against @astrojs/rss 4.0.18 (index.js:145,157): the helper sets
 * item.guid from `link` first, then Object.assign-merges parsed customData
 * over it, so our <guid> wins. If this breaks after an @astrojs/rss upgrade,
 * confirm that assignment order still holds.
 */
export function wpGuidCustomData(
  wp_guid: string | undefined,
  link: string,
  site: URL,
): string {
  const raw = wp_guid ?? new URL(link, site).toString();
  // Encode & as &amp; — only character that needs escaping in this attribute-
  // free text-node context (< and > don't appear in valid URLs).
  const safe = raw.replace(/&/g, '&amp;');
  return `<guid isPermaLink="false">${safe}</guid>`;
}
