@Component
public class RequestSigningFilter extends OncePerRequestFilter {

    @Override
    protected void doFilterInternal(
            HttpServletRequest request,
            HttpServletResponse response,
            FilterChain filterChain
    ) throws IOException, ServletException {

        try {
            var serviceId = request.getHeader("X-Service-Id");
            var timestamp = request.getHeader("X-Timestamp");
            var signature = request.getHeader("X-Signature");

            var secret = ServiceRegistry.getSecret(serviceId);
            if (secret == null) throw new Exception("Unknown service");

            var body = new String(request.getInputStream().readAllBytes());
            var expected = RequestSigner.sign(
                    secret,
                    request.getMethod(),
                    request.getRequestURI(),
                    timestamp,
                    body
            );

            if (!MessageDigest.isEqual(
                    expected.getBytes(),
                    signature.getBytes())) {
                throw new Exception("Invalid signature");
            }

            filterChain.doFilter(request, response);

        } catch (Exception e) {
            response.sendError(401, e.getMessage());
        }
    }
}