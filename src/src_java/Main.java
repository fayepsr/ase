import resolver.Python3Resolver;

import java.util.Arrays;

public class Main {
    public static void main(String[] args) {
        Python3Resolver resolver = new Python3Resolver();
        LTok[] lToks = resolver.lex("<input code as string >");
        System.out.println(Arrays.toString(lToks));
    }
}