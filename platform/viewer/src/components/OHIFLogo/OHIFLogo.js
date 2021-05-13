import './OHIFLogo.css';
import Logo from './Pulmorad-logo.png'

import { Icon } from '@ohif/ui';
import React from 'react';

function OHIFLogo() {
  return (
    <a
      target="_blank"
      rel="noopener noreferrer"
      className="header-brand"
      href="https://lamis.snuhpia.org"
    >
      <img src={Logo} alt="PULMORAD" className="header-logo-text" />
    </a>
  );
}

export default OHIFLogo;
