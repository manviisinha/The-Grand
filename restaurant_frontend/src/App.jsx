import React from 'react';
import './App.css';

function App() {
  return (
    <div className="container">
      <header className="header-typo">
        <a href="#home" className="logo-typo">The Grand</a>
        <nav className="nav-typo">
          <a href="#story">Our Story</a>
          <a href="#menu">A-La-Carte</a>
          <a href="#private">Private Dining</a>
        </nav>
        <a href="#booking" className="nav-typo book-btn-typo">Reservations</a>
      </header>

      <main>
        {/* ================= HERO (TYPOGRAPHY LED) ================= */}
        <section id="home" className="hero-typo">
          <div className="hero-subtitle">
            Est. 2026 &mdash; Fine Dining & Seafood
          </div>
          
          <div className="hero-headline-container">
            <h1 className="display-text line-1">Taste</h1>
            <h1 className="display-text line-2 text-italic">The Ocean's</h1>
            <h1 className="display-text line-3">Bounty.</h1>
          </div>
          
          <div className="hero-info">
            <div className="info-block">
              <span className="label">Location</span>
              <p>Taj Lands End, Bandra West.<br/>Mumbai, India.</p>
            </div>
            <div className="info-block" style={{ justifySelf: 'end' }}>
              <span className="label">Operating Hours</span>
              <p>Tuesday &mdash; Sunday<br/>11:00 AM &mdash; 11:30 PM</p>
            </div>
          </div>
        </section>

        {/* ================= EDITORIAL STORY SECTION ================= */}
        <section id="story" style={{ padding: '8rem 0', display: 'flex', gap: '5vw', alignItems: 'flex-start', borderBottom: '2px solid var(--text-primary)'}}>
          <h3 style={{ fontSize: 'clamp(2rem, 4vw, 4rem)', lineHeight: '1.2', maxWidth: '800px', fontStyle: 'italic' }}>
            We believe that a truly extraordinary dining experience is defined not by excess, but by the relentless pursuit of perfection in the simplest ingredients.
          </h3>
          <p style={{ maxWidth: '400px', fontSize: '1.2rem', color: 'var(--text-secondary)' }}>
            The Grand Restaurant strips away the unnecessary, bringing the freshest catches from the sea directly to your palate. Our culinary narrative is one of precision, passion, and profound respect for the ocean.
          </p>
        </section>

        {/* ================= MENU AS TYPOGRAPHY LIST ================= */}
        <section id="menu" className="menu-typo">
          <h2 className="menu-header">Menu Highlights</h2>
          
          <div className="menu-grid">
            {/* Column 1 */}
            <div className="menu-category">
              <h4>Starters</h4>
              <div className="menu-item"><span className="item-name">Paneer Tikka</span><span className="item-price">₹450</span></div>
              <div className="menu-item"><span className="item-name">Hara Bhara Kebab</span><span className="item-price">₹350</span></div>
              <div className="menu-item"><span className="item-name">Chicken Safed Murgh</span><span className="item-price">₹480</span></div>
              
              <h4 style={{marginTop: '4rem'}}>Tandoor</h4>
              <div className="menu-item"><span className="item-name">Tandoori Mixed Platter</span><span className="item-price">₹1200</span></div>
              <div className="menu-item"><span className="item-name">Mutton Seekh Kebab</span><span className="item-price">₹650</span></div>
            </div>

            {/* Column 2 */}
            <div className="menu-category">
              <h4>Mains</h4>
              <div className="menu-item"><span className="item-name">Butter Chicken</span><span className="item-price">₹550</span></div>
              <div className="menu-item"><span className="item-name">Dal Makhani</span><span className="item-price">₹400</span></div>
              <div className="menu-item"><span className="item-name">Mutton Rogan Josh</span><span className="item-price">₹680</span></div>
              
              <h4 style={{marginTop: '4rem'}}>Accompaniments</h4>
              <div className="menu-item"><span className="item-name">Garlic Naan</span><span className="item-price">₹80</span></div>
              <div className="menu-item"><span className="item-name">Jeera Rice</span><span className="item-price">₹150</span></div>
            </div>
          </div>
        </section>

        {/* ================= TYPOGRAPHIC BOOKING CTA ================= */}
        <section id="booking" className="booking-typo">
          <span className="label" style={{ marginBottom: '2rem', display: 'block' }}>Reservations</span>
          <h2>Secure Your Table.</h2>
          <p style={{ maxWidth: '500px', margin: '0 auto 4rem auto', fontSize: '1.2rem', color: 'var(--text-secondary)' }}>
            We leverage a seamlessly swift reservation system via our WhatsApp Concierge. Booking your table takes seconds.
          </p>
          
          <a href="https://wa.me/14155238886?text=join%20return-newspaper" target="_blank" rel="noopener noreferrer" className="whatsapp-typo-btn" style={{ padding: '12px 24px', fontSize: '1.1rem', maxWidth: '300px', margin: '0 auto' }}>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
              <path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.898-4.45 9.897-9.896 0-2.639-1.028-5.116-2.895-6.983-1.867-1.868-4.345-2.896-6.983-2.896-5.447 0-9.896 4.448-9.897 9.896-.001 1.914.59 3.81 1.636 5.421l-1.167 4.265 4.364-1.4zM16.592 12.016c-.22-.112-1.309-.646-1.511-.72-.202-.074-.35-.112-.497.108-.147.22-.572.72-.7.868-.128.148-.256.167-.476.056-2.316-1.161-3.665-2.222-4.9-4.307-.129-.22-.014-.339.096-.449.099-.1.22-.256.331-.384.111-.128.148-.22.221-.368.073-.148.037-.278-.018-.388-.055-.111-.497-1.205-.681-1.65-.18-.435-.363-.377-.497-.384-.128-.007-.276-.007-.424-.007-.148 0-.389.056-.592.278-.203.222-.774.757-.774 1.846 0 1.089.793 2.144.904 2.292.111.148 1.562 2.386 3.784 3.345.529.228.941.364 1.264.466.531.168 1.015.144 1.398.087.434-.065 1.309-.535 1.493-1.052.184-.518.184-.961.129-1.053-.055-.091-.202-.146-.423-.257z"/>
            </svg>
            Book via WhatsApp
          </a>
        </section>
      </main>

      <footer className="footer-typo">
        <div className="footer-top">
          <div className="footer-block">
            <h5>General Inquiries</h5>
            <p>hello@thegrand.in</p>
            <p>+91 22 6668 1234</p>
          </div>
          <div className="footer-block">
            <h5>Socials</h5>
            <a href="#">Instagram</a>
            <a href="#">Twitter</a>
          </div>
          <div className="footer-block">
            <h5>Address</h5>
            <p>Taj Lands End, Bandra West.<br/>Mumbai, Maharashtra.<br/>India.</p>
          </div>
        </div>
        <div className="footer-logo">
          The Grand
        </div>
        <div style={{ textAlign: 'center', marginTop: '2rem', fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
          &copy; {new Date().getFullYear()} The Grand. 
        </div>
      </footer>
    </div>
  );
}

export default App;
