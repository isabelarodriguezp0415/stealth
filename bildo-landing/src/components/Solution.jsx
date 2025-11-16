import React from 'react';
import { Brain, Zap, Target } from 'lucide-react';

const Solution = () => {
  return (
    <section id="solucion" className="py-24 gradient-primary">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid md:grid-cols-2 gap-12 items-center">
          {/* Left - Content */}
          <div className="text-white">
            <div className="inline-flex items-center space-x-2 bg-white/10 backdrop-blur-sm px-4 py-2 rounded-full mb-6">
              <Brain className="text-accent" size={20} />
              <span className="text-sm font-medium">Inteligencia Artificial</span>
            </div>

            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              La Solución que Cambia el Paradigma
            </h2>

            <p className="text-xl text-gray-300 mb-8 leading-relaxed">
              BILDO utiliza inteligencia artificial para realizar análisis normativo avanzado,
              transformando la complejidad del suelo en conocimiento, y el conocimiento en oportunidad.
            </p>

            <div className="space-y-6">
              <div className="flex items-start space-x-4">
                <div className="bg-accent rounded-lg p-3 flex-shrink-0">
                  <Brain className="text-white" size={24} />
                </div>
                <div>
                  <h3 className="text-xl font-bold mb-2">Análisis Automático</h3>
                  <p className="text-gray-300">
                    IA interpreta automáticamente decretos, normativas urbanas y datos catastrales.
                  </p>
                </div>
              </div>

              <div className="flex items-start space-x-4">
                <div className="bg-secondary rounded-lg p-3 flex-shrink-0">
                  <Zap className="text-white" size={24} />
                </div>
                <div>
                  <h3 className="text-xl font-bold mb-2">Resultados en Segundos</h3>
                  <p className="text-gray-300">
                    Calcula edificabilidad y potencial de desarrollo en cuestión de segundos, no días.
                  </p>
                </div>
              </div>

              <div className="flex items-start space-x-4">
                <div className="bg-accent rounded-lg p-3 flex-shrink-0">
                  <Target className="text-white" size={24} />
                </div>
                <div>
                  <h3 className="text-xl font-bold mb-2">Decisiones Informadas</h3>
                  <p className="text-gray-300">
                    Información técnica, precisa y visual para decisiones estratégicas rentables.
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Right - Visual Element */}
          <div className="relative">
            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20">
              <div className="text-white space-y-6">
                <div className="border-l-4 border-accent pl-4">
                  <div className="text-sm text-gray-400 mb-1">INPUT</div>
                  <div className="font-semibold">Datos Catastrales + Normativa</div>
                </div>

                <div className="flex items-center justify-center py-4">
                  <div className="flex items-center space-x-3">
                    <div className="w-3 h-3 bg-accent rounded-full animate-pulse"></div>
                    <div className="w-3 h-3 bg-accent rounded-full animate-pulse delay-75"></div>
                    <div className="w-3 h-3 bg-accent rounded-full animate-pulse delay-150"></div>
                  </div>
                </div>

                <div className="bg-accent/20 rounded-lg p-4 text-center">
                  <Brain className="inline-block text-accent mb-2" size={32} />
                  <div className="font-bold">Análisis con IA</div>
                  <div className="text-sm text-gray-400 mt-1">Procesamiento Automático</div>
                </div>

                <div className="flex items-center justify-center py-4">
                  <div className="flex items-center space-x-3">
                    <div className="w-3 h-3 bg-secondary rounded-full animate-pulse"></div>
                    <div className="w-3 h-3 bg-secondary rounded-full animate-pulse delay-75"></div>
                    <div className="w-3 h-3 bg-secondary rounded-full animate-pulse delay-150"></div>
                  </div>
                </div>

                <div className="border-l-4 border-secondary pl-4">
                  <div className="text-sm text-gray-400 mb-1">OUTPUT</div>
                  <div className="font-semibold mb-2">Oportunidades Priorizadas</div>
                  <div className="grid grid-cols-2 gap-2 text-sm">
                    <div className="bg-white/5 rounded px-2 py-1">Edificabilidad</div>
                    <div className="bg-white/5 rounded px-2 py-1">Potencial</div>
                    <div className="bg-white/5 rounded px-2 py-1">Restricciones</div>
                    <div className="bg-white/5 rounded px-2 py-1">Visualización</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Solution;
