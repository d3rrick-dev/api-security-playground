public class RequestSigner {

    public static String sign(
            String secret,
            String method,
            String path,
            String timestamp,
            String body
    ) throws Exception {

        var canonical = String.join("\n",
                method.toUpperCase(),
                path,
                timestamp,
                sha256(body)
        );

        var mac = Mac.getInstance("HmacSHA256");
        mac.init(new SecretKeySpec(secret.getBytes(), "HmacSHA256"));
        return HexFormat.of().formatHex(mac.doFinal(canonical.getBytes()));
    }

    private static String sha256(String data) throws Exception {
        var digest = MessageDigest.getInstance("SHA-256");
        return HexFormat.of().formatHex(digest.digest(data.getBytes()));
    }
}