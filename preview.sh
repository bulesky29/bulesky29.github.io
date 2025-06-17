mkdir -p tianyi_site/content/post
mkdir -p tianyi_site/content/archive
\rm -r tianyi_site/content/post
\rm -r tianyi_site/content/archive
mkdir -p tianyi_site/content/post
mkdir -p tianyi_site/content/archive
hugo mod tidy --source tianyi_site
obsidian-export --ignore archive vaults/blog tianyi_site/content/post
obsidian-export vaults/blog/archive tianyi_site/content/archive
hugo server --source tianyi_site -D