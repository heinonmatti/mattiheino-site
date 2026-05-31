import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

// Shared schema for both registers. `image()` is provided by the schema
// context so infographics get Astro's asset pipeline (AVIF/WebP, hashing).
const postSchema = ({ image }: { image: () => any }) =>
  z.object({
    title: z.string(),
    description: z.string(),
    lang: z.enum(['en', 'fi']).default('en'),

    // Immutable original publication date.
    published: z.coerce.date(),
    // Set when a legacy post is re-read for ongoing relevance; equals
    // `published` for native posts written today.
    vetted_on: z.coerce.date().optional(),
    // Internal backlog tracker. Never rendered to readers.
    vetting_status: z.enum(['pending', 'done']).default('pending'),

    migration_source: z
      .enum(['native', 'mattiheino-wp', 'motivationselfmanagement'])
      .default('native'),

    infographic: z
      .object({
        src: image(),
        alt: z.string(),
        prompt: z.string().optional(),
      })
      .optional(),

    social_copy: z
      .object({
        linkedin: z.string().optional(),
        x: z.string().optional(),
        facebook: z.string().optional(),
        bluesky: z.string().optional(),
        instagram: z.string().optional(),
        whatsapp_channel: z.string().optional(),
        whatsapp_status: z.string().optional(),
      })
      .optional(),
    // queued -> the cross-poster Action fans out on next push, then flips to posted.
    social_status: z.enum(['skip', 'queued', 'posted']).default('skip'),

    // Cross-links between the two registers.
    rigorous_companion: z.string().optional(),
    applied_companion: z.string().optional(),

    // Per-post record of images lost in migration, etc.
    migration_notes: z.string().optional(),

    // true only for un-vetted motivationselfmanagement.com imports.
    draft: z.boolean().default(false),
    tags: z.array(z.string()).default([]),
  });

const posts = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/posts' }),
  schema: postSchema,
});

const appliedMusings = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/applied-musings' }),
  schema: postSchema,
});

export const collections = {
  posts,
  'applied-musings': appliedMusings,
};
