mkdir -p tianyi_site/content/post
mkdir -p tianyi_site/content/archives
mkdir -p tmp
\rm -r tianyi_site/content/post
\rm -r tianyi_site/content/archives
\rm -r tmp
mkdir -p tianyi_site/content/post
mkdir -p tianyi_site/content/archives
mkdir -p tmp
hugo mod tidy --source tianyi_site
cp -r vaults/blog tmp
rm -r tmp/blog/00-template
obsidian-export tmp/blog tianyi_site/content/post
mv tianyi_site/content/post/archives/* tianyi_site/content/archives
rm -r tianyi_site/content/post/archives
mv tianyi_site/content/post/about.md tianyi_site/content
mv tianyi_site/content/post/friend.md tianyi_site/content
hugo server --source tianyi_site