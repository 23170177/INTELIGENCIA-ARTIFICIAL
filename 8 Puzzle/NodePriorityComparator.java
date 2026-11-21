import java.util.Comparator;

public class NodePriorityComparator implements Comparator<Node> {

    @Override
    public int compare(Node primero, Node segundo) {
        int costoA = primero.getCost();
        int costoB = segundo.getCost();

        if (costoA < costoB) {
            return -1;
        }
        if (costoA > costoB) {
            return 1;
        }
        return 0;
    }
}

