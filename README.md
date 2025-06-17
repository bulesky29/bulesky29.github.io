
```bash
\rm -r tianyi_site/content/posts
mkdir -p tianyi_site/content/posts
hugo mod tidy
obsidian-export vaults/blog tianyi_site/content/posts
hugo server --source tianyi_site
```