import React from 'react';
import { Link } from 'react-router-dom';

const LandingPage = () => {
  return (
    <section className="landing-page">
      <div className="landing-top">
        <p className="landing-eyebrow">Digital Voter Registration</p>
        <Link className="landing-admin-link" to="/admin">
          Admin
        </Link>
      </div>

      <div className="landing-intro">
        <h1>Simple voter registration for everyone.</h1>
        <p className="landing-description">
          Use this platform to submit your voter details online in a few minutes, then track your status
          at any time. We support multiple channels so registration remains accessible on smartphones,
          feature phones, and messaging apps.
        </p>
      </div>

      <div className="channel-info">
        <h3>Other registration channels</h3>
        <p><strong>USSD:</strong> Dial <code>*384*99767#</code> and follow prompts (name, ID, county, voter choice).</p>
        <p><strong>WhatsApp:</strong> Send <code>join frighten-zebra</code> to <code>+1 415 523 8886</code>, then send <code>menu</code> and follow the registration prompts.</p>
      </div>

      <div className="landing-actions">
        <Link className="landing-btn primary" to="/register">
          Register Now
        </Link>
        <Link className="landing-btn" to="/check-status">
          Check Status
        </Link>
      </div>
    </section>
  );
};

export default LandingPage;
