"""SPLIX: modelo celular simplificado con ADN dividido en ADNm, ADNa y ADNi."""
from __future__ import annotations
import random
import threading
import queue
import time
from typing import Dict, Any, List

class ADNm:
    """Atributos genéticos primarios de SPLIX."""

    def __init__(self, genes: Dict[str, int] | None = None) -> None:
        self.genes = genes or {
            "fuerza": 5,
            "curacion": 3,
            "metabolismo": 4,
            "curiosidad": 5,
            "resistencia": 4,
            "reproducir": 5,
            "adaptabilidad": 4,
            "eficiencia": 4,
            "virus": 1,
            "mutacion": 3,
        }

    def valor(self, nombre: str, defecto: int = 1) -> int:
        return self.genes.get(nombre, defecto)

    def __repr__(self) -> str:
        return f"ADNm({self.genes})"


class ADNa:
    """Atributos dinámicos de estado, energía y glucosa."""

    def __init__(self, adnm: ADNm) -> None:
        self.adnm = adnm
        self.energia = 20
        self.atp = 12
        self.glucosa = 10
        self.salud = 18
        self.edad = 0
        self.infectado = False
        self.virus_ciclos = 0

    def actualizar(self, energia: int = 0, atp: int = 0, glucosa: int = 0, salud: int = 0) -> None:
        self.energia = max(0, self.energia + energia)
        self.atp = max(0, self.atp + atp)
        self.glucosa = max(0, self.glucosa + glucosa)
        self.salud = max(0, min(30, self.salud + salud))

    def esta_viva(self) -> bool:
        return self.energia > 0 and self.salud > 0

    def __repr__(self) -> str:
        return (
            f"ADNa(energia={self.energia}, atp={self.atp}, glucosa={self.glucosa}, "
            f"salud={self.salud}, edad={self.edad}, infectado={self.infectado}, virus_ciclos={self.virus_ciclos})"
        )


class ADNi:
    """Genera procesos y funciones celulares con base en el ADN."""

    def __init__(self, adnm: ADNm, adna: ADNa) -> None:
        self.adnm = adnm
        self.adna = adna

    def generar_procesos(self) -> List[str]:
        pasos: List[str] = []
        if self.adnm.valor("metabolismo") >= 3:
            pasos.append("generar_atp")
        if self.adnm.valor("fuerza") >= 5:
            pasos.append("defender")
        if self.adnm.valor("curacion") >= 3:
            pasos.append("autocurar")
        if self.adnm.valor("curiosidad") >= 4:
            pasos.append("explorar")
        if self.adnm.valor("resistencia") >= 4:
            pasos.append("reparar_danio")
        if self.adnm.valor("reproducir") >= 4:
            pasos.append("reproducir")
        if self.adnm.valor("adaptabilidad") >= 4:
            pasos.append("ajustar_entorno")
        if self.adnm.valor("eficiencia") >= 4:
            pasos.append("optimizar")
        if not pasos:
            pasos.append("generar_atp")
        return pasos

    def procesar_comando(self, comando: str) -> List[str]:
        comando = comando.strip().lower()
        if comando == "":
            return []
        if comando.startswith("gene "):
            partes = comando.split()
            if len(partes) == 3 and partes[2].isdigit():
                return [f"ajustar_gene:{partes[1]}:{partes[2]}"]
        if comando.startswith("estado "):
            partes = comando.split()
            if len(partes) == 4 and all(p.isdigit() for p in partes[1:]):
                return [f"ajustar_estado:{partes[1]}:{partes[2]}:{partes[3]}"]
        if comando == "status":
            return ["mostrar_estado"]
        if comando == "help":
            return ["mostrar_ayuda"]
        if comando.startswith("virus ") or comando == "virus":
            objetivo = comando[6:].strip()
            if objetivo.startswith('"') and objetivo.endswith('"'):
                objetivo = objetivo[1:-1]
            elif objetivo.startswith("'") and objetivo.endswith("'"):
                objetivo = objetivo[1:-1]
            return [f"virus:{objetivo}"]
        if comando == "q" or comando == "salir":
            return ["detener"]
        if comando.startswith("alimentar"):
            partes = comando.split()
            cantidad = int(partes[1]) if len(partes) > 1 and partes[1].isdigit() else 5
            return [f"alimentar:{cantidad}"]
        return ["comando_desconocido"]


class ADN:
    """Contenedor de ADNm, ADNa y ADNi."""

    def __init__(self, genes: Dict[str, int] | None = None) -> None:
        self.adnm = ADNm(genes)
        self.adna = ADNa(self.adnm)
        self.adni = ADNi(self.adnm, self.adna)

    def transcribir(self, comando: str = "") -> "ARNm":
        instrucciones = self.adni.generar_procesos() + self.adni.procesar_comando(comando)
        return ARNm(instrucciones)

    def __repr__(self) -> str:
        return f"ADN(adnm={self.adnm}, adna={self.adna})"


class ARNm:
    """Mensajero ARN con todos los procesos de la célula."""

    def __init__(self, instrucciones: List[str]) -> None:
        self.instrucciones = instrucciones
        self.errores = [False] * len(instrucciones)

    def degradar(self) -> None:
        for i in range(len(self.instrucciones)):
            if random.random() < 0.08:
                self.instrucciones[i] = random.choice([
                    "generar_atp",
                    "defender",
                    "autocurar",
                    "explorar",
                    "reparar_danio",
                    "reproducir",
                    "optimizar",
                ])
                self.errores[i] = True

    def reparar(self, adn: ADN) -> None:
        for i, instr in enumerate(self.instrucciones):
            if self.errores[i] and instr not in adn.adni.generar_procesos():
                self.instrucciones[i] = adn.adni.generar_procesos()[i % len(adn.adni.generar_procesos())]
                self.errores[i] = False

    def traducir(self) -> List[str]:
        return list(self.instrucciones)

    def __repr__(self) -> str:
        return f"ARNm(instrucciones={self.instrucciones}, errores={sum(self.errores)})"


class Entorno:
    """Entorno externo que provee glucosa, virus y genera peligro."""

    def __init__(self) -> None:
        self.glucosa = 20
        self.peligro = 4
        self.virus = 2
        self.luz = True
        self.agua = True

    def actualizar(self) -> None:
        self.glucosa = max(0, self.glucosa - random.randint(0, 3))
        self.peligro = min(10, max(0, self.peligro + random.randint(-1, 2)))
        self.virus = min(10, max(0, self.virus + random.randint(-1, 2)))
        self.luz = random.random() < 0.8
        self.agua = random.random() < 0.75
        if self.virus > 6:
            self.peligro = min(10, self.peligro + 1)

    def contagiar(self, forma: "Forma") -> None:
        if self.virus <= 0:
            return
        if random.random() < 0.2 + self.virus * 0.05:
            forma.adn.adna.actualizar(salud=-1, atp=-1)
            if self.virus > 7:
                forma.adn.adna.actualizar(energia=-1)
            print(f"{forma.nombre} sufrió efecto viral. Virus presente: {self.virus}")

    def ofrecer_glucosa(self, cantidad: int) -> int:
        tomado = min(self.glucosa, cantidad)
        self.glucosa -= tomado
        return tomado

    def __repr__(self) -> str:
        return (
            f"Entorno(glucosa={self.glucosa}, peligro={self.peligro}, "
            f"virus={self.virus}, luz={self.luz}, agua={self.agua})"
        )


class Organulo:
    """Base simple para organelos celulares."""

    def ejecutar(self, instruccion: str, celula: "Forma") -> None:
        raise NotImplementedError


class Nucleo(Organulo):
    def __init__(self, adn: ADN) -> None:
        self.adn = adn

    def producir_arnm(self, comando: str) -> ARNm:
        arnm = self.adn.transcribir(comando)
        arnm.degradar()
        arnm.reparar(self.adn)
        return arnm


class Mitocondria(Organulo):
    def producir_atp(self, celula: "Forma") -> int:
        base = celula.adn.adnm.valor("metabolismo") * 2
        extra = celula.adn.adnm.valor("eficiencia")
        if celula.adn.adna.glucosa > 0:
            glucosa_usada = min(celula.adn.adna.glucosa, 3)
            celula.adn.adna.actualizar(glucosa=-glucosa_usada, atp=glucosa_usada)
            return max(1, base + extra)
        return max(1, base // 2)


class Ribosoma(Organulo):
    def traducir(self, arnm: ARNm) -> List[str]:
        return arnm.traducir()


class Membrana(Organulo):
    def intercambiar(self, celula: "Forma", entorno: Entorno) -> None:
        if entorno.glucosa > 0:
            tomado = entorno.ofrecer_glucosa(4)
            celula.adn.adna.actualizar(glucosa=tomado)

    def recibir_danio(self, celula: "Forma", entorno: Entorno) -> None:
        if entorno.peligro > 6:
            celula.adn.adna.actualizar(salud=-(entorno.peligro - 5))
        if entorno.virus > 5 and random.random() < 0.3:
            celula.adn.adna.actualizar(salud=-1)
            print(f"{celula.nombre} recibió daño viral a través de la membrana.")


class Citoplasma(Organulo):
    def ejecutar(self, instruccion: str, celula: "Forma", entorno: Entorno) -> None:
        adna = celula.adn.adna
        adnm = celula.adn.adnm
        if instruccion == "generar_atp":
            produced = Mitocondria().producir_atp(celula)
            adna.actualizar(atp=produced)
        elif instruccion == "defender":
            if adna.atp >= 2:
                adna.actualizar(atp=-2)
            else:
                adna.actualizar(salud=-1)
        elif instruccion == "autocurar":
            cost = 3
            if adna.atp >= cost:
                adna.actualizar(atp=-cost, salud=adnm.valor("curacion"))
        elif instruccion == "explorar":
            if adna.atp >= 2:
                adna.actualizar(atp=-2)
                Membrana().intercambiar(celula, entorno)
        elif instruccion == "reparar_danio":
            if adna.atp >= 3:
                adna.actualizar(atp=-3, salud=2)
        elif instruccion == "reproducir":
            if adna.energia >= 25 and adna.salud >= 20 and adna.atp >= 5:
                adna.actualizar(atp=-5, energia=-10)
                celula.reproducirse = True
        elif instruccion == "ajustar_entorno":
            if adna.atp >= 2:
                adna.actualizar(atp=-2)
                entorno.peligro = max(0, entorno.peligro - 1)
        elif instruccion == "optimizar":
            if adna.atp >= 1:
                adna.actualizar(atp=-1, energia=1)
        elif instruccion.startswith("ajustar_gene:"):
            _, nombre, valor = instruccion.split(":")
            celula.adn.adnm.genes[nombre] = max(1, min(10, int(valor)))
        elif instruccion.startswith("ajustar_estado:"):
            _, energia, salud, edad = instruccion.split(":")
            adna.energia = max(0, int(energia))
            adna.salud = max(0, min(30, int(salud)))
            adna.edad = max(0, int(edad))
        elif instruccion.startswith("alimentar:"):
            _, cantidad = instruccion.split(":")
            adna.actualizar(glucosa=int(cantidad))
        elif instruccion == "mostrar_estado":
            celula.mostrar_estado()
        elif instruccion == "detener":
            celula.activo = False
        elif instruccion == "acelerar":
            for i in range(4):
                self.salud -= 4
                arnm = celula.nucleo.producir_arnm("")
                instrucciones = celula.ribosoma.traducir(arnm)
                for instr in instrucciones:
                    self.ejecutar(instr, celula, entorno)
                    if not celula.activo:
                        break
                if not celula.activo:
                    break
        elif instruccion == "mostrar_ayuda":
            print(
                "Comandos disponibles:\n"
                "  help                  Mostrar esta ayuda.\n"
                "  status                Ver estado de SPLIX y los hijos.\n"
                "  q | salir | exit      Salir del simulador.\n"
                "  alimentar [cantidad]  Añade glucosa.\n"
                "  gene <gen> <valor>    Cambia un gen de 1 a 10.\n"
                "  estado <e> <s> <edad> Ajusta energía, salud y edad.\n"
                "  kill <nombre>         Elimina una forma específica.\n"
                "  matar <nombre>        Igual que kill.\n"
                "  hijo <nombre> <comando> Envía un comando solo al hijo.\n"
                "  virus \"nombre\"      Intenta infectar al objetivo y agrega virus al entorno.\n"
                "  <nombre> <comando>    Atajo para dirigir un comando a una forma.\n"
            )
        match instruccion:
            case "comando_desconocido":
                adna.actualizar(salud=-1)
        match instruccion:
            case "generar_atp":
                print(f"SPLIX generó ATP. ATP actual: {adna.atp}")
            case "defender":
                print(f"SPLIX se defendió. Salud actual: {adna.salud}")
            case "autocurar":
                print(f"SPLIX se autocuró. Salud actual: {adna.salud}")
            case "explorar":
                print(f"SPLIX exploró el entorno. Glucosa actual: {adna.glucosa}")
            case "reparar_danio":
                print(f"SPLIX reparó daño. Salud actual: {adna.salud}")
            case "reproducir":
                print("SPLIX se preparó para reproducirse.")
            case "ajustar_entorno":
                print(f"SPLIX ajustó el entorno. Peligro actual: {entorno.peligro}")
            case "optimizar":
                print(f"SPLIX optimizó su metabolismo. Energía actual: {adna.energia}")
            case "comando_desconocido":
                print("SPLIX recibió un comando desconocido y perdió salud.")  
            case kill if kill.startswith("ajustar_gene:"):
                _, nombre, valor = kill.split(":")
                print(f"SPLIX ajustó el gen {nombre} a {valor}.")
            case estado if estado.startswith("ajustar_estado:"):
                _, energia, salud, edad = estado.split(":")
                print(f"SPLIX ajustó su estado a energía={energia}, salud={salud}, edad={edad}.")
            case "mostrar_estado":
                celula.mostrar_estado()
            case "detener":
                print("SPLIX se detuvo por comando.")
            case  "matar SPLIX}":
                celula.activo = False
                print("SPLIX fue eliminado.")


class Forma:
    """Representa una forma viva con organelos y ADN."""

    def __init__(self, nombre: str, adn: ADN) -> None:
        self.nombre = nombre
        self.adn = adn
        self.nucleo = Nucleo(adn)
        self.ribosoma = Ribosoma()
        self.citoplasma = Citoplasma()
        self.membrana = Membrana()
        self.activo = True
        self.reproducirse = False

    def ciclo(self, comando: str, entorno: Entorno) -> None:
        self.adn.adna.edad += 1
        self.membrana.intercambiar(self, entorno)
        arnm = self.nucleo.producir_arnm(comando)
        instrucciones = self.ribosoma.traducir(arnm)
        for instr in instrucciones:
            self.citoplasma.ejecutar(instr, self, entorno)
            if not self.activo:
                break
        self.membrana.recibir_danio(self, entorno)
        self.adn.adna.actualizar(atp=-1)
        if self.adn.adna.atp < 2:
            self.adn.adna.actualizar(salud=-1)
        if self.adn.adna.energia < 5:
            self.adn.adna.actualizar(salud=-1)
        if self.adn.adna.infectado:
            fuerza_virus = self.adn.adnm.valor("virus")
            self.adn.adna.actualizar(energia=-1, atp=-1)
            if fuerza_virus >= 1:
                entorno.virus = min(10, entorno.virus + 1)
            self.adn.adna.virus_ciclos += 1
            print(f"{self.nombre} está infectado; ciclo viral {self.adn.adna.virus_ciclos}/5.")
            if self.adn.adna.virus_ciclos >= 5:
                self.activo = False
                entorno.virus = min(10, entorno.virus + 5)
                print(f"{self.nombre} murió tras 5 ciclos de infección y liberó virus al entorno.")

    def mostrar_estado(self) -> None:
        print(f"{self.nombre}: {self.adn.adna}")
        print(self.adn.adnm)

    def __repr__(self) -> str:
        return f"Forma({self.nombre}, {self.adn.adna})"


class Estructura:
    """Contiene las formas vivas y el entorno compartido."""

    def __init__(self, forma: Forma) -> None:
        self.formas: List[Forma] = [forma]
        self.entorno = Entorno()

    def _buscar_forma(self, nombre: str) -> Forma | None:
        for forma in self.formas:
            if forma.nombre.lower() == nombre.lower():
                return forma
        return None

    def _matar_forma(self, nombre: str) -> None:
        objetivo = self._buscar_forma(nombre)
        if objetivo:
            objetivo.activo = False
            print(f"{objetivo.nombre} fue eliminado por comando externo.")
        else:
            print(f"No se encontró forma para matar: {nombre}")

    def ejecutar(self, comando: str) -> None:
        objetivo = None
        comando_activo = comando.strip()
        if comando_activo:
            partes = comando_activo.split(maxsplit=1)
            palabra = partes[0].lower()
            if palabra in {"kill", "matar"} and len(partes) > 1:
                self._matar_forma(partes[1])
                return
            if palabra in {"hijo", "child"} and len(partes) > 1:
                subpartes = partes[1].split(maxsplit=1)
                if len(subpartes) > 1:
                    objetivo = subpartes[0]
                    comando_activo = subpartes[1]
                else:
                    print("Formato de comando hijo inválido. Usa: hijo <nombre> <comando>")
                    objetivo = None
                    comando_activo = ""
            elif self._buscar_forma(partes[0]) is not None and len(partes) > 1:
                objetivo = partes[0]
                comando_activo = partes[1]

        if comando_activo.lower().startswith("virus"):
            virus_partes = comando_activo.split(maxsplit=1)
            objetivo_virus = ""
            if len(virus_partes) > 1:
                objetivo_virus = virus_partes[1].strip()
                if objetivo_virus.startswith('"') and objetivo_virus.endswith('"'):
                    objetivo_virus = objetivo_virus[1:-1]
                elif objetivo_virus.startswith("'") and objetivo_virus.endswith("'"):
                    objetivo_virus = objetivo_virus[1:-1]
            objetivo_forma = self._buscar_forma(objetivo_virus)
            if objetivo_forma:
                fuerza_virus = objetivo_forma.adn.adnm.valor("virus")
                if random.random() < 0.5 or fuerza_virus == 10:
                    if fuerza_virus == 10:
                        objetivo_forma.activo = False
                        self.entorno.virus = min(10, self.entorno.virus + 5)
                        print(f"{objetivo_forma.nombre} fue destruido por un virus de potencia 10 y liberó virus al entorno.")
                    else:
                        objetivo_forma.adn.adna.actualizar(salud=-2, atp=-2, energia=-1)
                        objetivo_forma.adn.adna.infectado = True
                        objetivo_forma.adn.adna.virus_ciclos = 0
                        self.entorno.virus = min(10, self.entorno.virus + max(1, fuerza_virus))
                        print(f"{objetivo_forma.nombre} fue infectado por virus. Virus agregado: {max(1, fuerza_virus)}")
                else:
                    print(f"Intento de infección sobre {objetivo_forma.nombre} falló.")
            else:
                print("No se encontró objetivo de virus.")
            return

        self.entorno.actualizar()
        infectados = sum(1 for forma in self.formas if forma.activo and forma.adn.adna.infectado)
        if infectados > 0:
            self.entorno.virus = min(10, self.entorno.virus + infectados * 5)
        nuevas: List[Forma] = []
        for forma in list(self.formas):
            if not forma.activo or not forma.adn.adna.esta_viva():
                forma.activo = False
                continue
            self.entorno.contagiar(forma)
            if objetivo is None:
                forma.ciclo(comando_activo, self.entorno)
            elif forma.nombre.lower() == objetivo.lower():
                forma.ciclo(comando_activo, self.entorno)
            else:
                forma.ciclo("", self.entorno)
            if forma.reproducirse:
                hijo_adn = forma.adn.adna.adnm.genes.copy()
                nueva = Forma(f"{forma.nombre}_hijo", ADN(hijo_adn))
                nuevas.append(nueva)
                forma.reproducirse = False
        self.formas.extend(nuevas)
        self.formas = [f for f in self.formas if f.activo and f.adn.adna.esta_viva()]

    def estado_general(self) -> None:
        print(self.entorno)
        for forma in self.formas:
            print(forma)


def main() -> None:
    splix = Forma("SPLIX", ADN())
    universo = Estructura(splix)
    print("SPLIX inicia con ADNa, ADNm y ADNi. Ejecutando ciclos continuos; escribe 'q' para salir.")

    cmd_queue: "queue.Queue[str]" = queue.Queue()
    stop_event = threading.Event()

    def input_loop(q: "queue.Queue[str]", stop: threading.Event) -> None:
        while not stop.is_set():
            try:
                cmd = input("Comando: ")
            except EOFError:
                stop.set()
                break
            if cmd:
                q.put(cmd)
            if cmd.lower() in {"q", "salir", "exit"}:
                stop.set()
                break

    th = threading.Thread(target=input_loop, args=(cmd_queue, stop_event), daemon=True)
    th.start()

    try:
        while not stop_event.is_set() and splix.activo and splix.adn.adna.esta_viva():
            comando = ""
            try:
                comando = cmd_queue.get_nowait()
            except queue.Empty:
                comando = ""

            if comando.lower() in {"q", "salir", "exit"}:
                break

            universo.ejecutar(comando)
            universo.estado_general()

            if not universo.formas:
                print("Todas las formas han dejado de vivir.")
                break

            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Simulación interrumpida por usuario.")
    finally:
        stop_event.set()
        th.join(timeout=1)



if __name__ == "__main__":
    main()
