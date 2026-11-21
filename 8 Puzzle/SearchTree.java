import java.util.ArrayDeque;
import java.util.Deque;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.PriorityQueue;
import java.util.Set;

public class SearchTree {

    private static final int MAX_PATH_TO_PRINT = 60;

    private final String endState;
    private final Node root;

    public SearchTree(String initialState, String endState) {
        this.root = new Node(initialState, null);
        this.endState = endState;
    }

    private boolean esMeta(Node nodo) {
        return endState.equals(nodo.getState());
    }

    private void printResults(String nombreAlgoritmo, int profundidad, int procesados,
                              int generados, long startTime) {
        double segundos = (System.currentTimeMillis() - startTime) / 1000.0;

        System.out.println("=======================================");
        System.out.println("RESULTADOS: " + nombreAlgoritmo);
        System.out.println("Meta encontrada en profundidad: " + profundidad);
        System.out.println("Nodos procesados (evaluados): " + procesados);
        System.out.println("Nodos generados (creados): " + generados);
        System.out.println("Tiempo real: " + segundos + " segundos");
        System.out.println("=======================================");
    }

    private void printPath(Node meta) {
        LinkedList<Node> recorrido = new LinkedList<>();

        for (Node actual = meta; actual != null; actual = actual.getParent()) {
            recorrido.addFirst(actual);
        }

        System.out.println("Estado meta encontrado: " + meta.getState());

        if (recorrido.size() > MAX_PATH_TO_PRINT) {
            System.out.println("El camino tiene " + (recorrido.size() - 1)
                    + " pasos (demasiado largo para imprimirlo).");
            return;
        }

        for (Node paso : recorrido) {
            System.out.println(NodeUtils.formatState(paso.getState()));
        }
    }

    private int expandirSinCosto(Node actual, Set<String> visitados,
                                 Deque<Node> frontera) {
        int creados = 0;
        for (Node hijo : NodeUtils.generateChildren(actual)) {
            if (!visitados.contains(hijo.getState())) {
                frontera.add(hijo);
                creados++;
            }
        }
        return creados;
    }

    public void iterativeDeepeningSearch(int maxDepth) {
        long inicio = System.currentTimeMillis();
        int evaluados = 0;
        int generados = 0;

        for (int limite = 0; limite <= maxDepth; limite++) {
            Map<String, Integer> visitados = new HashMap<>();
            Deque<Node> pila = new ArrayDeque<>();

            pila.push(root);
            generados++;
            visitados.put(root.getState(), root.getDepth());

            while (!pila.isEmpty()) {
                evaluados++;
                Node actual = pila.pop();

                if (esMeta(actual)) {
                    System.out.println("Límite de profundidad donde se encontró: " + limite);
                    printPath(actual);
                    printResults("Búsqueda iterativa en profundidad", actual.getDepth(),
                            evaluados, generados, inicio);
                    return;
                }

                if (actual.getDepth() >= limite) {
                    continue;
                }

                for (Node hijo : NodeUtils.generateChildren(actual)) {
                    Integer profundidadPrevia = visitados.get(hijo.getState());
                    if (profundidadPrevia == null || hijo.getDepth() < profundidadPrevia) {
                        visitados.put(hijo.getState(), hijo.getDepth());
                        pila.push(hijo);
                        generados++;
                    }
                }
            }

            System.out.println("Límite " + limite + ": sin solución");
        }

        System.out.println("No se encontró solución dentro del límite: " + maxDepth);
    }

    public void uniformCostSearch() {
        long inicio = System.currentTimeMillis();
        int evaluados = 0;
        int generados = 0;

        Set<String> visitados = new HashSet<>();
        PriorityQueue<Node> frontera = new PriorityQueue<>(new NodePriorityComparator());

        frontera.add(root);
        generados++;

        while (!frontera.isEmpty()) {
            evaluados++;
            Node actual = frontera.poll();

            if (!visitados.add(actual.getState())) {
                continue;
            }

            if (esMeta(actual)) {
                printPath(actual);
                printResults("Búsqueda de costo uniforme", actual.getDepth(),
                        evaluados, generados, inicio);
                return;
            }

            for (Node hijo : NodeUtils.generateChildren(actual)) {
                if (!visitados.contains(hijo.getState())) {
                    hijo.setCost(actual.getDepth() + 1);
                    frontera.add(hijo);
                    generados++;
                }
            }
        }

        System.out.println("No se encontró solución con costo uniforme.");
    }

    public void deepFirstSearch() {
        long inicio = System.currentTimeMillis();
        int evaluados = 0;
        int generados = 0;

        Set<String> visitados = new HashSet<>();
        Deque<Node> pila = new ArrayDeque<>();

        pila.push(root);
        generados++;

        while (!pila.isEmpty()) {
            evaluados++;
            Node actual = pila.pop();

            if (!visitados.add(actual.getState())) {
                continue;
            }

            if (esMeta(actual)) {
                printPath(actual);
                printResults("Búsqueda en profundidad", actual.getDepth(),
                        evaluados, generados, inicio);
                return;
            }

            List<Node> hijos = NodeUtils.generateChildren(actual);
            for (int i = hijos.size() - 1; i >= 0; i--) {
                Node hijo = hijos.get(i);
                if (!visitados.contains(hijo.getState())) {
                    pila.push(hijo);
                    generados++;
                }
            }
        }

        System.out.println("No se encontró solución con búsqueda en profundidad.");
    }

    public void breadthFirstSearch() {
        long inicio = System.currentTimeMillis();
        int evaluados = 0;
        int generados = 0;

        Set<String> visitados = new HashSet<>();
        Deque<Node> cola = new ArrayDeque<>();

        cola.add(root);
        generados++;

        while (!cola.isEmpty()) {
            evaluados++;
            Node actual = cola.poll();

            if (!visitados.add(actual.getState())) {
                continue;
            }

            if (esMeta(actual)) {
                printPath(actual);
                printResults("Búsqueda primero en anchura", actual.getDepth(),
                        evaluados, generados, inicio);
                return;
            }

            generados += expandirSinCosto(actual, visitados, cola);
        }

        System.out.println("No se encontró solución con búsqueda en anchura.");
    }
}

