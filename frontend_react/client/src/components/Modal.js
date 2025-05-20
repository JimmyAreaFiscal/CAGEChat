import React from 'react';

const Modal = ({ children, onClose }) => (
  <div className="modal-overlay">
    <div className="modal modal-3d">
      <button className="modal-close" onClick={onClose}>×</button>
      {children}
    </div>
  </div>
);

export default Modal; 