import React, { useState } from 'react';
import { Send, CheckCircle, Building2, Mail, User, Phone } from 'lucide-react';

const CTA = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    company: '',
    message: '',
  });

  const [isSubmitted, setIsSubmitted] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Aquí iría la lógica de envío del formulario
    console.log('Form submitted:', formData);
    setIsSubmitted(true);
    setTimeout(() => setIsSubmitted(false), 3000);
  };

  return (
    <section id="contacto" className="py-24 gradient-primary">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid md:grid-cols-2 gap-12 items-center">
          {/* Left - Content */}
          <div className="text-white">
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              Descubre el Potencial de tu Próximo Proyecto
            </h2>

            <p className="text-xl text-gray-300 mb-8">
              Solicita una demostración personalizada y descubre cómo BILDO puede
              transformar la forma en que identificas oportunidades inmobiliarias.
            </p>

            <div className="space-y-4 mb-8">
              <div className="flex items-center space-x-3">
                <CheckCircle className="text-accent flex-shrink-0" size={24} />
                <span>Demo personalizada de 30 minutos</span>
              </div>
              <div className="flex items-center space-x-3">
                <CheckCircle className="text-accent flex-shrink-0" size={24} />
                <span>Análisis de prueba de uno de tus lotes</span>
              </div>
              <div className="flex items-center space-x-3">
                <CheckCircle className="text-accent flex-shrink-0" size={24} />
                <span>Consultoría sin costo sobre casos de uso</span>
              </div>
              <div className="flex items-center space-x-3">
                <CheckCircle className="text-accent flex-shrink-0" size={24} />
                <span>Sin compromiso ni tarjeta de crédito</span>
              </div>
            </div>

            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20">
              <div className="text-sm text-gray-300 mb-2">Empresas que confían en BILDO</div>
              <div className="flex items-center space-x-6">
                <div className="text-2xl font-bold">🏗️</div>
                <div className="text-2xl font-bold">🏢</div>
                <div className="text-2xl font-bold">🏘️</div>
                <div className="text-sm text-gray-400">+20 constructoras</div>
              </div>
            </div>
          </div>

          {/* Right - Form */}
          <div className="bg-white rounded-2xl p-8 shadow-2xl">
            {!isSubmitted ? (
              <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                  <label htmlFor="name" className="block text-sm font-semibold text-primary mb-2">
                    Nombre Completo *
                  </label>
                  <div className="relative">
                    <User className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                    <input
                      type="text"
                      id="name"
                      name="name"
                      required
                      value={formData.name}
                      onChange={handleChange}
                      className="w-full pl-11 pr-4 py-3 border-2 border-gray-200 rounded-lg focus:border-accent focus:outline-none transition-colors"
                      placeholder="Juan Pérez"
                    />
                  </div>
                </div>

                <div>
                  <label htmlFor="email" className="block text-sm font-semibold text-primary mb-2">
                    Email Corporativo *
                  </label>
                  <div className="relative">
                    <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                    <input
                      type="email"
                      id="email"
                      name="email"
                      required
                      value={formData.email}
                      onChange={handleChange}
                      className="w-full pl-11 pr-4 py-3 border-2 border-gray-200 rounded-lg focus:border-accent focus:outline-none transition-colors"
                      placeholder="juan@empresa.com"
                    />
                  </div>
                </div>

                <div>
                  <label htmlFor="phone" className="block text-sm font-semibold text-primary mb-2">
                    Teléfono
                  </label>
                  <div className="relative">
                    <Phone className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                    <input
                      type="tel"
                      id="phone"
                      name="phone"
                      value={formData.phone}
                      onChange={handleChange}
                      className="w-full pl-11 pr-4 py-3 border-2 border-gray-200 rounded-lg focus:border-accent focus:outline-none transition-colors"
                      placeholder="+57 300 123 4567"
                    />
                  </div>
                </div>

                <div>
                  <label htmlFor="company" className="block text-sm font-semibold text-primary mb-2">
                    Empresa *
                  </label>
                  <div className="relative">
                    <Building2 className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                    <input
                      type="text"
                      id="company"
                      name="company"
                      required
                      value={formData.company}
                      onChange={handleChange}
                      className="w-full pl-11 pr-4 py-3 border-2 border-gray-200 rounded-lg focus:border-accent focus:outline-none transition-colors"
                      placeholder="Constructora ABC"
                    />
                  </div>
                </div>

                <div>
                  <label htmlFor="message" className="block text-sm font-semibold text-primary mb-2">
                    ¿En qué podemos ayudarte?
                  </label>
                  <textarea
                    id="message"
                    name="message"
                    rows="4"
                    value={formData.message}
                    onChange={handleChange}
                    className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-accent focus:outline-none transition-colors resize-none"
                    placeholder="Cuéntanos sobre tu proyecto o necesidades..."
                  ></textarea>
                </div>

                <button
                  type="submit"
                  className="w-full bg-gradient-accent text-white py-4 rounded-lg font-bold text-lg hover:shadow-xl transition-all transform hover:scale-105 flex items-center justify-center space-x-2"
                >
                  <span>Solicitar Demo Gratuita</span>
                  <Send size={20} />
                </button>

                <p className="text-sm text-gray-500 text-center">
                  Al enviar el formulario, aceptas nuestra política de privacidad
                </p>
              </form>
            ) : (
              <div className="text-center py-12">
                <div className="bg-accent/10 rounded-full w-20 h-20 flex items-center justify-center mx-auto mb-6">
                  <CheckCircle className="text-accent" size={40} />
                </div>
                <h3 className="text-2xl font-bold text-primary mb-3">
                  ¡Solicitud Recibida!
                </h3>
                <p className="text-gray-600">
                  Nos pondremos en contacto contigo en las próximas 24 horas para agendar tu demo.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </section>
  );
};

export default CTA;
