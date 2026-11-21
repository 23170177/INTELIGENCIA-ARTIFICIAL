public class App {

    public static void main(String[] args) {
        final String estadoMeta = "12345678 ";
        final String estadoInicial = "7621 8435";

        System.out.println("ESTADO META:\n" + NodeUtils.formatState(estadoMeta));
        System.out.println("ESTADO INICIAL:\n" + NodeUtils.formatState(estadoInicial));

        SearchTree arbol = new SearchTree(estadoInicial, estadoMeta);

        arbol.breadthFirstSearch();
        arbol.deepFirstSearch();
        arbol.uniformCostSearch();
        arbol.iterativeDeepeningSearch(50);
    }
}

