import React from 'react';
import { ArrowRight, Sparkles } from 'lucide-react';

const Hero = () => {
  return (
    <section className="relative min-h-screen flex items-center gradient-primary overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute inset-0" style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.4'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
        }}></div>
      </div>

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-32">
        <div className="grid md:grid-cols-2 gap-12 items-center">
          {/* Left Content */}
          <div className="text-white">
            <div className="inline-flex items-center space-x-2 bg-white/10 backdrop-blur-sm px-4 py-2 rounded-full mb-6">
              <Sparkles className="text-accent" size={20} />
              <span className="text-sm font-medium">Análisis Normativo con IA</span>
            </div>

            <h1 className="text-5xl md:text-6xl font-bold mb-6 leading-tight">
              Transforma la normativa en{' '}
              <span className="text-accent">oportunidades</span>
            </h1>

            <p className="text-xl text-gray-300 mb-8 leading-relaxed">
              BILDO analiza automáticamente la normativa urbana con IA, calcula edificabilidad
              e identifica el potencial de desarrollo de cada lote en segundos.
            </p>

            <div className="flex flex-col sm:flex-row gap-4">
              <a
                href="#contacto"
                className="inline-flex items-center justify-center bg-accent hover:bg-accent-dark text-white px-8 py-4 rounded-lg font-semibold text-lg transition-all transform hover:scale-105 shadow-xl"
              >
                Solicitar Demo Gratuita
                <ArrowRight className="ml-2" size={20} />
              </a>
              <a
                href="#como-funciona"
                className="inline-flex items-center justify-center bg-white/10 backdrop-blur-sm hover:bg-white/20 text-white px-8 py-4 rounded-lg font-semibold text-lg transition-all border border-white/20"
              >
                Ver Cómo Funciona
              </a>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-3 gap-8 mt-12 pt-12 border-t border-white/20">
              <div>
                <div className="text-3xl font-bold text-accent mb-1">90%</div>
                <div className="text-sm text-gray-300">Reducción de tiempo</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-accent mb-1">99%</div>
                <div className="text-sm text-gray-300">Precisión</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-accent mb-1">24/7</div>
                <div className="text-sm text-gray-300">Disponibilidad</div>
              </div>
            </div>
          </div>

          {/* Right Content - Visual */}
          <div className="hidden md:block">
            <div className="relative">
              {/* Floating Card Mockup */}
              <div className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20 shadow-2xl">
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-white font-semibold">Análisis de Lote</span>
                    <div className="bg-accent/20 text-accent px-3 py-1 rounded-full text-sm font-medium">
                      Completado
                    </div>
                  </div>

                  <div className="h-48 bg-gradient-to-br from-accent/20 to-secondary/20 rounded-lg flex items-center justify-center">
                    <div className="text-center text-white">
                      <div className="text-5xl font-bold mb-2">2,847m²</div>
                      <div className="text-sm text-gray-300">Edificabilidad Máxima</div>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-white/5 rounded-lg p-4">
                      <div className="text-gray-400 text-xs mb-1">Altura Máxima</div>
                      <div className="text-white font-semibold">18 pisos</div>
                    </div>
                    <div className="bg-white/5 rounded-lg p-4">
                      <div className="text-gray-400 text-xs mb-1">Uso de Suelo</div>
                      <div className="text-white font-semibold">Mixto</div>
                    </div>
                  </div>

                  <div className="bg-accent/20 border border-accent/30 rounded-lg p-4">
                    <div className="text-accent text-sm font-semibold">
                      Potencial: Alto - Zona en desarrollo
                    </div>
                  </div>
                </div>
              </div>

              {/* Floating Elements */}
              <div className="absolute -top-4 -right-4 bg-accent rounded-full w-24 h-24 flex items-center justify-center shadow-xl animate-pulse">
                <Sparkles className="text-white" size={32} />
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
