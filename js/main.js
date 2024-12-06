// Version management
let currentVersions = [];

async function loadVersions() {
    try {
        const response = await fetch('/api/versions');
        currentVersions = await response.json();
        populateVersionSelector();
    } catch (error) {
        console.error('Failed to load versions:', error);
    }
}

function populateVersionSelector() {
    const select = document.getElementById('version-select');
    select.innerHTML = ''; // Clear existing options
    
    // Add latest version
    const latestOption = document.createElement('option');
    latestOption.value = 'latest';
    latestOption.textContent = 'Latest Version';
    select.appendChild(latestOption);
    
    // Add other versions
    currentVersions.forEach(version => {
        const option = document.createElement('option');
        option.value = version.id;
        option.textContent = `Version ${version.number} (${version.date})`;
        select.appendChild(option);
    });
}

async function downloadSelected() {
    const select = document.getElementById('version-select');
    const version = select.value;
    
    try {
        const response = await fetch(`/api/download/${version}`);
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `mysticscape-${version}.exe`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            a.remove();
        } else {
            throw new Error('Download failed');
        }
    } catch (error) {
        console.error('Download failed:', error);
        alert('Failed to download. Please try again later.');
    }
}

// Blog management
async function loadBlogPosts() {
    try {
        const response = await fetch('/api/blog/posts');
        const posts = await response.json();
        displayBlogPosts(posts);
    } catch (error) {
        console.error('Failed to load blog posts:', error);
    }
}

function displayBlogPosts(posts) {
    const blogGrid = document.querySelector('.blog-grid');
    blogGrid.innerHTML = ''; // Clear existing posts
    
    posts.forEach(post => {
        const article = document.createElement('article');
        article.className = 'blog-post';
        article.innerHTML = `
            <h3>${post.title}</h3>
            <p class="post-meta">By ${post.author} on ${new Date(post.date).toLocaleDateString()}</p>
            <p class="post-excerpt">${post.excerpt}</p>
            <a href="/blog/${post.slug}" class="read-more">Read More</a>
        `;
        blogGrid.appendChild(article);
    });
}

// Navigation
document.addEventListener('DOMContentLoaded', () => {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Load initial data
    loadVersions();
    loadBlogPosts();
});
