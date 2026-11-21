import java.util.ArrayList;
import java.util.List;

public class NodeUtils {

    private static final int[][] MOVIMIENTOS = {
            {1, 3},
            {0, 2, 4},
            {1, 5},
            {0, 4, 6},
            {1, 3, 5, 7},
            {2, 4, 8},
            {3, 7},
            {4, 6, 8},
            {5, 7}
    };

    private NodeUtils() {
    }

    public static String formatState(String state) {
        StringBuilder tablero = new StringBuilder(state.length() * 2);

        for (int i = 0; i < state.length(); i++) {
            tablero.append(state.charAt(i));
            tablero.append(' ');
            if ((i + 1) % 3 == 0) {
                tablero.append('\n');
            }
        }

        return tablero.toString();
    }

    public static List<Node> generateChildren(Node parentNode) {
        String actual = parentNode.getState();
        int hueco = actual.indexOf(' ');
        List<Node> hijos = new ArrayList<>(MOVIMIENTOS[hueco].length);

        for (int destino : MOVIMIENTOS[hueco]) {
            hijos.add(new Node(intercambiar(actual, hueco, destino), parentNode));
        }

        return hijos;
    }

    private static String intercambiar(String state, int origen, int destino) {
        char[] piezas = state.toCharArray();
        char temporal = piezas[origen];
        piezas[origen] = piezas[destino];
        piezas[destino] = temporal;
        return String.valueOf(piezas);
    }
}
