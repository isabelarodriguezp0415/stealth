import React from 'react';
import { Linkedin, Twitter, Mail, MapPin } from 'lucide-react';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-primary text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid md:grid-cols-4 gap-8 mb-8">
          {/* Brand */}
          <div className="md:col-span-2">
            <div className="text-3xl font-bold mb-4">
              BILDO<span className="text-accent">.</span>
            </div>
            <p className="text-gray-400 mb-4 max-w-md">
              Transformamos la complejidad normativa en oportunidades inmobiliarias
              mediante inteligencia artificial.
            </p>
            <div className="flex space-x-4">
              <a
                href="#"
                className="bg-white/10 hover:bg-accent p-2 rounded-lg transition-colors"
              >
                <Linkedin size={20} />
              </a>
              <a
                href="#"
                className="bg-white/10 hover:bg-accent p-2 rounded-lg transition-colors"
              >
                <Twitter size={20} />
              </a>
              <a
                href="#"
                className="bg-white/10 hover:bg-accent p-2 rounded-lg transition-colors"
              >
                <Mail size={20} />
              </a>
            </div>
          </div>

          {/* Links */}
          <div>
            <h4 className="font-bold mb-4">Producto</h4>
            <ul className="space-y-2 text-gray-400">
              <li><a href="#caracteristicas" className="hover:text-accent transition-colors">Características</a></li>
              <li><a href="#como-funciona" className="hover:text-accent transition-colors">Cómo Funciona</a></li>
              <li><a href="#beneficios" className="hover:text-accent transition-colors">Beneficios</a></li>
              <li><a href="#" className="hover:text-accent transition-colors">Precios</a></li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h4 className="font-bold mb-4">Contacto</h4>
            <ul className="space-y-3 text-gray-400">
              <li className="flex items-start space-x-2">
                <Mail className="flex-shrink-0 mt-1" size={16} />
                <span>contacto@bildo.ai</span>
              </li>
              <li className="flex items-start space-x-2">
                <MapPin className="flex-shrink-0 mt-1" size={16} />
                <span>Bogotá, Colombia</span>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-white/10 pt-8 flex flex-col md:flex-row justify-between items-center">
          <div className="text-gray-400 text-sm mb-4 md:mb-0">
            © {currentYear} BILDO. Todos los derechos reservados.
          </div>
          <div className="flex space-x-6 text-sm text-gray-400">
            <a href="#" className="hover:text-accent transition-colors">
              Términos y Condiciones
            </a>
            <a href="#" className="hover:text-accent transition-colors">
              Política de Privacidad
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
