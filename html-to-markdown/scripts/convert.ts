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
    
    // Process article content
    if (data.content && data.content !== null) {
      const title = data.title || 'Untitled';
      const filename = sanitizeFilename(title);
      const markdown = htmlToMarkdown(data.content);
      
      const metadata: PageMetadata = {
        url: data.url || '',
        title: title,
        source: data.source || 'unknown',
        published: data.publish_time || '',
        type: 'article',
      };
      
      if (data.description) {
        metadata.description = data.description;
      }
      
      const frontmatter = formatMetadataYaml(metadata);
      const fullContent = `${frontmatter}\n\n${markdown}`;
      
      const outputPath = join(dir, `${filename}.md`);
      writeFileSync(outputPath, fullContent, 'utf-8');
      
      const wordCount = markdown.split(/\s+/).length;
      const headingCount = (markdown.match(/^#+\s/gm) || []).length;
      console.log(`  ✓ ${filename}.md (words: ${wordCount}, headings: ${headingCount})`);
      articles++;
    }
    
    // Process discussion content
    const additionalMeta = data.additional_metadata || {};
    if (additionalMeta.comments_content && additionalMeta.comments_content !== null) {
      const title = data.title || 'Untitled';
      const filename = sanitizeFilename(title);
      const markdown = htmlToMarkdown(additionalMeta.comments_content);
      
      const metadata: PageMetadata = {
        url: additionalMeta.comments_url || '',
        title: `${title} - Discussion`,
        source: data.source || 'hacker_news',
        type: 'hn_discussion',
        original_article: data.url || '',
      };
      
      if (additionalMeta.points) metadata.points = additionalMeta.points;
      if (additionalMeta.comments) metadata.comments = additionalMeta.comments;
      
      const frontmatter = formatMetadataYaml(metadata);
      const fullContent = `${frontmatter}\n\n${markdown}`;
      
      const outputPath = join(dir, `${filename}-discussion.md`);
      writeFileSync(outputPath, fullContent, 'utf-8');
      
      const wordCount = markdown.split(/\s+/).length;
      const headingCount = (markdown.match(/^#+\s/gm) || []).length;
      console.log(`  ✓ ${filename}-discussion.md (words: ${wordCount}, headings: ${headingCount})`);
      discussions++;
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
