import './style.css';
import { featuredProjectIds, projects, siteData } from './portfolioData';

const app = document.querySelector('#app');

const projectMap = new Map(projects.map((project) => [project.id, project]));
const featuredProjects = featuredProjectIds.map((id) => projectMap.get(id)).filter(Boolean);
const techStack = [...new Set(projects.flatMap((project) => project.tech))].sort((a, b) =>
  a.localeCompare(b),
);

const renderTech = (tech) => tech.map((item) => `<li class="chip">${item}</li>`).join('');

const renderProjectCard = (project) => `
  <article class="project-card reveal">
    <p class="project-category">${project.category}</p>
    <h3>${project.title}</h3>
    <p>${project.description}</p>
    <ul class="chip-list" aria-label="Technologies used in ${project.title}">
      ${renderTech(project.tech)}
    </ul>
    <div class="card-footer">
      <span class="status-badge" aria-label="Project status ${project.status}">✅ ${project.status}</span>
      <a class="inline-link" href="${project.url}" target="_blank" rel="noreferrer">View on GitHub</a>
    </div>
  </article>
`;

app.innerHTML = `
  <a class="skip-link" href="#main-content">Skip to content</a>
  <header class="site-header">
    <div class="container nav-wrap">
      <a class="brand" href="#top">${siteData.name}</a>
      <nav aria-label="Primary navigation">
        <ul>
          <li><a href="#projects">Projects</a></li>
          <li><a href="#skills">Skills</a></li>
          <li><a href="#about">About</a></li>
          <li><a href="#contact">Contact</a></li>
        </ul>
      </nav>
    </div>
  </header>

  <main id="main-content">
    <section id="top" class="hero">
      <div class="container hero-grid">
        <div class="hero-copy reveal">
          <p class="kicker">AI Portfolio</p>
          <h1>${siteData.name}</h1>
          <p class="subtitle">${siteData.role} • ${siteData.location}</p>
          <p class="lead">${siteData.headline}</p>
          <div class="hero-actions">
            <a class="btn btn-primary" href="#projects">Explore Projects</a>
            <a class="btn btn-secondary" href="${siteData.repository}" target="_blank" rel="noreferrer">Repository</a>
          </div>
        </div>
        <aside class="hero-panel reveal" aria-label="Portfolio highlights">
          <h2>At a glance</h2>
          <ul>
            <li><strong>18+</strong> AI application repositories</li>
            <li><strong>Core focus:</strong> RAG, NLP, Gemini, LangChain, Streamlit</li>
            <li><strong>Major build:</strong> SIH finalist project VOJAS</li>
          </ul>
        </aside>
      </div>
      <div class="orb orb-one" aria-hidden="true"></div>
      <div class="orb orb-two" aria-hidden="true"></div>
    </section>

    <section class="section" id="projects" aria-labelledby="projects-heading">
      <div class="container">
        <div class="section-heading reveal">
          <p class="kicker">Selected work</p>
          <h2 id="projects-heading">Featured AI Projects</h2>
          <p>Highlighted projects from the repository with production-focused AI workflows.</p>
        </div>
        <div class="project-grid">
          ${featuredProjects.map(renderProjectCard).join('')}
        </div>
      </div>
    </section>

    <section class="section muted" aria-labelledby="all-projects-heading">
      <div class="container">
        <div class="section-heading reveal">
          <h2 id="all-projects-heading">All Repository Projects</h2>
          <p>Complete portfolio index sourced from this repository.</p>
        </div>
        <div class="project-grid compact">
          ${projects.map(renderProjectCard).join('')}
        </div>
      </div>
    </section>

    <section class="section" id="skills" aria-labelledby="skills-heading">
      <div class="container">
        <div class="section-heading reveal">
          <h2 id="skills-heading">Skills & Technology</h2>
          <p>Technology focus represented across the portfolio projects.</p>
        </div>
        <ul class="chip-list skill-list reveal" aria-label="Skills list">
          ${renderTech(techStack)}
        </ul>
      </div>
    </section>

    <section class="section muted" id="about" aria-labelledby="about-heading">
      <div class="container about-grid">
        <div class="section-heading reveal">
          <h2 id="about-heading">About</h2>
          <p>${siteData.about}</p>
          <p class="about-links">
            <a class="inline-link" href="${siteData.linkedin}" target="_blank" rel="noreferrer">LinkedIn</a>
            <span aria-hidden="true">•</span>
            <a class="inline-link" href="${siteData.githubProfile}" target="_blank" rel="noreferrer">GitHub</a>
          </p>
        </div>
        <article class="major-project reveal" aria-labelledby="major-project-heading">
          <h3 id="major-project-heading">${siteData.majorProject.title}</h3>
          <p>${siteData.majorProject.description}</p>
          <div class="hero-actions">
            <a class="btn btn-secondary" href="${siteData.majorProject.liveUrl}" target="_blank" rel="noreferrer">Live Project</a>
            <a class="btn btn-secondary" href="${siteData.majorProject.githubUrl}" target="_blank" rel="noreferrer">Source</a>
          </div>
        </article>
      </div>
    </section>

    <section class="section contact" id="contact" aria-labelledby="contact-heading">
      <div class="container reveal">
        <h2 id="contact-heading">Let’s collaborate on AI products</h2>
        <p>Open to collaboration, internships, and AI product opportunities.</p>
        <a class="btn btn-primary" href="mailto:${siteData.email}">Contact: ${siteData.email}</a>
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <div class="container">
      <p>© ${new Date().getFullYear()} ${siteData.name}. Built from repository source data.</p>
      <a class="inline-link" href="${siteData.repository}" target="_blank" rel="noreferrer">
        ${siteData.repository}
      </a>
    </div>
  </footer>
`;

const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

if (!reducedMotion) {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.2 },
  );

  document.querySelectorAll('.reveal').forEach((element) => observer.observe(element));
} else {
  document.querySelectorAll('.reveal').forEach((element) => element.classList.add('is-visible'));
}
