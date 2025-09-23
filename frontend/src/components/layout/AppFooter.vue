<template>
  <footer class="app-footer">
    <div class="footer-container">
      <div class="footer-content">
        <div class="footer-section">
          <h3 class="footer-title">Global Team Manager</h3>
          <p class="footer-description">
            Coordinate your distributed team across different timezones and schedule meetings efficiently.
          </p>
        </div>
        
        <div class="footer-section">
          <h4 class="footer-subtitle">Features</h4>
          <ul class="footer-links">
            <li><a href="#" class="footer-link">Team Management</a></li>
            <li><a href="#" class="footer-link">Meeting Scheduler</a></li>
            <li><a href="#" class="footer-link">Timezone Support</a></li>
            <li><a href="#" class="footer-link">Availability Calendar</a></li>
          </ul>
        </div>
        
        <div class="footer-section">
          <h4 class="footer-subtitle">Support</h4>
          <ul class="footer-links">
            <li><a href="#" class="footer-link">Documentation</a></li>
            <li><a href="#" class="footer-link">Help Center</a></li>
            <li><a href="#" class="footer-link">Contact Us</a></li>
          </ul>
        </div>
      </div>
      
      <div class="footer-bottom">
        <p class="footer-copyright">
          © 2024 Global Team Manager. Built with Vue.js and FastAPI.
        </p>
      </div>
    </div>
  </footer>
</template>

<script setup>
// Footer component - no additional logic needed
</script>

<style scoped>
.app-footer {
  background: #1e293b;
  color: #94a3b8;
  margin-top: auto;
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 20px 1rem;
}

.footer-content {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: 2rem;
  margin-bottom: 2rem;
}

.footer-section {
  display: flex;
  flex-direction: column;
}

.footer-title {
  color: white;
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0 0 0.5rem 0;
}

.footer-subtitle {
  color: white;
  font-size: 1rem;
  font-weight: 500;
  margin: 0 0 1rem 0;
}

.footer-description {
  font-size: 0.9rem;
  line-height: 1.6;
  margin: 0;
}

.footer-links {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-links li {
  margin-bottom: 0.5rem;
}

.footer-link {
  color: #94a3b8;
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.2s ease;
}

.footer-link:hover {
  color: white;
}

.footer-bottom {
  border-top: 1px solid #334155;
  padding-top: 1rem;
  text-align: center;
}

.footer-copyright {
  font-size: 0.85rem;
  margin: 0;
}

@media (max-width: 768px) {
  .footer-content {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .footer-container {
    padding: 1.5rem 20px 1rem;
  }
}
</style>
