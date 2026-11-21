public class Node implements Comparable<Node> {

    private int cost;
    private int depth;
    private Node parent;
    private String state;

    public Node(String state, Node parent) {
        this.state = state;
        this.parent = parent;
        this.cost = 0;
        this.depth = parent == null ? 0 : parent.depth + 1;
    }

    public Node(String state, Node parent, int depth, int cost) {
        this.state = state;
        this.parent = parent;
        this.depth = depth;
        this.cost = cost;
    }

    public Node() {
        this(null, null, 0, 0);
    }

    @Override
    public int compareTo(Node other) {
        return Integer.compare(depth, other.depth);
    }

    public int getCost() {
        return cost;
    }

    public void setCost(int cost) {
        this.cost = cost;
    }

    public int getDepth() {
        return depth;
    }

    public void setDepth(int depth) {
        this.depth = depth;
    }

    public Node getParent() {
        return parent;
    }

    public void setParent(Node parent) {
        this.parent = parent;
    }

    public String getState() {
        return state;
    }

    public void setState(String state) {
        this.state = state;
    }
}

