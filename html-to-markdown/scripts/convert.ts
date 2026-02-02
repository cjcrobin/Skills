#!/usr/bin/env bun
/**
 * Convert HTML/JSON files to markdown format with frontmatter.
 * Usage: bun convert.ts <input-directory>
 * 
 * This script imports conversion utilities from html-to-markdown.ts
 * and adds CLI logic for batch file processing.
 */

import { readFileSync, writeFileSync, readdirSync, statSync } from 'fs';
import { join, basename, extname, dirname } from 'path';
import { htmlToMarkdown } from './html-to-markdown';

interface PageMetadata {
  url: string;
  title: string;
  description?: string;
  author?: string;
  published?: string;
  captured_at?: string;
  source?: string;
  type?: string;
  [key: string]: any;
}

function formatMetadataYaml(meta: PageMetadata): string {
  const lines = ['---'];
  
  for (const [key, value] of Object.entries(meta)) {
    if (value === undefined || value === null) continue;
    
    if (typeof value === 'string') {
      const escaped = value.replace(/"/g, '\\"');
      lines.push(`${key}: "${escaped}"`);
    } else {
      lines.push(`${key}: ${value}`);
    }
  }
  
  lines.push('---');
  return lines.join('\n');
}

function sanitizeFilename(title: string, maxLength: number = 80): string {
  let filename = title.toLowerCase();
  filename = filename.replace(/[^a-z0-9]+/g, '-');
  filename = filename.replace(/^-+|-+$/g, '');
  if (filename.length > maxLength) {
    filename = filename.substring(0, maxLength).replace(/-+$/, '');
  }
  return filename;
}

function processJsonFile(filePath: string): { articles: number; discussions: number } {
  try {
    const content = readFileSync(filePath, 'utf-8');
    const data = JSON.parse(content);
    
    let articles = 0;
    let discussions = 0;
    const dir = dirname(filePath);
    const source = data.source || 'unknown';
    const title = data.title || 'Untitled';
    
    // Detect source type and process accordingly
    if (source === 'hacker_news') {
      // Hacker News: post_content -> post.md, comment_content -> comment.md
      
      // Process post content
      if (data.post_content && data.post_content !== null) {
        const markdown = htmlToMarkdown(data.post_content);
        
        const metadata: PageMetadata = {
          url: data.post_url || '',
          title: title,
          source: 'hacker_news',
          published: data.publish_time || '',
          type: 'article',
          points: data.points || 0,
          num_comments: data.num_comments || 0,
        };
        
        const frontmatter = formatMetadataYaml(metadata);
        const fullContent = `${frontmatter}\n\n${markdown}`;
        
        const outputPath = join(dir, 'post.md');
        writeFileSync(outputPath, fullContent, 'utf-8');
        
        const wordCount = markdown.split(/\s+/).length;
        const headingCount = (markdown.match(/^#+\s/gm) || []).length;
        console.log(`  ✓ post.md (words: ${wordCount}, headings: ${headingCount})`);
        articles++;
      } else {
        console.log(`  ⚠ Skipping post.md: post_content is null`);
      }
      
      // Process comment content
      if (data.comment_content && data.comment_content !== null) {
        const markdown = htmlToMarkdown(data.comment_content);
        
        const metadata: PageMetadata = {
          url: data.comment_url || '',
          title: `${title} - Discussion`,
          source: 'hacker_news',
          type: 'hn_discussion',
          original_article: data.post_url || '',
          points: data.points || 0,
          num_comments: data.num_comments || 0,
        };
        
        const frontmatter = formatMetadataYaml(metadata);
        const fullContent = `${frontmatter}\n\n${markdown}`;
        
        const outputPath = join(dir, 'comment.md');
        writeFileSync(outputPath, fullContent, 'utf-8');
        
        const wordCount = markdown.split(/\s+/).length;
        const headingCount = (markdown.match(/^#+\s/gm) || []).length;
        console.log(`  ✓ comment.md (words: ${wordCount}, headings: ${headingCount})`);
        discussions++;
      } else {
        console.log(`  ⚠ Skipping comment.md: comment_content is null`);
      }
      
    } else if (source === 'product_hunt') {
      // Product Hunt: product_content -> product.md, hunt_content -> hunt.md
      
      // Process product content
      if (data.product_content && data.product_content !== null) {
        const markdown = htmlToMarkdown(data.product_content);
        
        const metadata: PageMetadata = {
          url: data.product_url || '',
          title: title,
          source: 'product_hunt',
          published: data.publish_time || '',
          type: 'product_page',
          votes: data.votes || 0,
        };
        
        const frontmatter = formatMetadataYaml(metadata);
        const fullContent = `${frontmatter}\n\n${markdown}`;
        
        const outputPath = join(dir, 'product.md');
        writeFileSync(outputPath, fullContent, 'utf-8');
        
        const wordCount = markdown.split(/\s+/).length;
        const headingCount = (markdown.match(/^#+\s/gm) || []).length;
        console.log(`  ✓ product.md (words: ${wordCount}, headings: ${headingCount})`);
        articles++;
      } else {
        console.log(`  ⚠ Skipping product.md: product_content is null`);
      }
      
      // Process hunt content
      if (data.hunt_content && data.hunt_content !== null) {
        const markdown = htmlToMarkdown(data.hunt_content);
        
        const metadata: PageMetadata = {
          url: data.hunt_url || '',
          title: `${title} - Product Hunt`,
          source: 'product_hunt',
          type: 'product_hunt_page',
          original_product: data.product_url || '',
          votes: data.votes || 0,
        };
        
        const frontmatter = formatMetadataYaml(metadata);
        const fullContent = `${frontmatter}\n\n${markdown}`;
        
        const outputPath = join(dir, 'hunt.md');
        writeFileSync(outputPath, fullContent, 'utf-8');
        
        const wordCount = markdown.split(/\s+/).length;
        const headingCount = (markdown.match(/^#+\s/gm) || []).length;
        console.log(`  ✓ hunt.md (words: ${wordCount}, headings: ${headingCount})`);
        discussions++;
      } else {
        console.log(`  ⚠ Skipping hunt.md: hunt_content is null`);
      }
      
    } else {
      // Unknown source or legacy format - try to handle gracefully
      console.log(`  ⚠ Unknown source '${source}' - attempting generic processing`);
      
      // Try legacy format first (content field)
      if (data.content && data.content !== null) {
        const filename = sanitizeFilename(title);
        const markdown = htmlToMarkdown(data.content);
        
        const metadata: PageMetadata = {
          url: data.url || '',
          title: title,
          source: source,
          published: data.publish_time || '',
          type: 'article',
        };
        
        const frontmatter = formatMetadataYaml(metadata);
        const fullContent = `${frontmatter}\n\n${markdown}`;
        
        const outputPath = join(dir, `${filename}.md`);
        writeFileSync(outputPath, fullContent, 'utf-8');
        console.log(`  ✓ ${filename}.md (legacy format)`);
        articles++;
      }
    }
    
    return { articles, discussions };
  } catch (error) {
    console.error(`✗ Error processing ${basename(filePath)}: ${error}`);
    return { articles: 0, discussions: 0 };
  }
}

function findFiles(dir: string, extensions: string[]): string[] {
  const files: string[] = [];
  
  try {
    const entries = readdirSync(dir);
    
    for (const entry of entries) {
      const fullPath = join(dir, entry);
      const stat = statSync(fullPath);
      
      if (stat.isDirectory()) {
        files.push(...findFiles(fullPath, extensions));
      } else if (stat.isFile()) {
        const ext = extname(entry);
        if (extensions.includes(ext)) {
          files.push(fullPath);
        }
      }
    }
  } catch (error) {
    console.error(`Error reading directory ${dir}: ${error}`);
  }
  
  return files;
}

function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.error('Usage: bun convert.ts <input-directory>');
    process.exit(1);
  }
  
  const inputDir = args[0];
  
  console.log('\n📝 Converting files to Markdown...');
  console.log(`   Input directory: ${inputDir}\n`);
  
  // Find all JSON files
  const jsonFiles = findFiles(inputDir, ['.json']);
  
  if (jsonFiles.length === 0) {
    console.log('✗ No JSON files found');
    process.exit(0);
  }
  
  let totalArticles = 0;
  let totalDiscussions = 0;
  let skipped = 0;
  
  for (const file of jsonFiles) {
    console.log(`Processing: ${basename(file)}`);
    const { articles, discussions } = processJsonFile(file);
    totalArticles += articles;
    totalDiscussions += discussions;
    if (articles === 0 && discussions === 0) {
      skipped++;
    }
  }
  
  console.log(`\n${'='.repeat(60)}`);
  console.log(`✓ Processed ${jsonFiles.length} files`);
  console.log(`✓ Generated ${totalArticles + totalDiscussions} markdown files`);
  console.log(`  - ${totalArticles} articles`);
  if (totalDiscussions > 0) {
    console.log(`  - ${totalDiscussions} discussions`);
  }
  if (skipped > 0) {
    console.log(`✗ Skipped ${skipped} files (null content)`);
  }
  console.log(`${'='.repeat(60)}\n`);
}

main();
