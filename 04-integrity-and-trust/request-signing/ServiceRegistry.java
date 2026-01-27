public class ServiceRegistry {

    private static final Map<String, String> SERVICES = Map.of(
            "order-service", "order-secret",
            "payment-service", "payment-secret"
    );

    public static String getSecret(String serviceId) {
        return SERVICES.get(serviceId);
    }
}