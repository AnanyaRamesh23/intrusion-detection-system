import streamlit as st
import joblib

# Load model
model = joblib.load("ids_model.joblib")

st.title("🛡️ Intrusion Detection System")
st.markdown("### 🔍 Enter network parameters to analyze traffic")

# Inputs
duration = st.number_input("Duration", min_value=0)
src_bytes = st.number_input("Source Bytes", min_value=0)
dst_bytes = st.number_input("Destination Bytes", min_value=0)
failed_logins = st.number_input("Failed Login Attempts", min_value=0)
connections = st.number_input("Connections", min_value=0)

# Button
if st.button("Check Traffic"):
    
    bytes_ratio = src_bytes / (dst_bytes + 1)

    sample = [[duration, src_bytes, dst_bytes, failed_logins, connections, bytes_ratio]]
    prediction = model.predict(sample)

    # Rule-based override (important upgrade)
    rule_flag = (
        (dst_bytes == 0 and src_bytes > 10000) or
        failed_logins > 5 or
        connections > 200
    )

    st.subheader("Result")

    if prediction[0] == 1 or rule_flag:
        st.error("⚠️ Intrusion Detected!")

        if rule_flag:
            st.caption("Rule-based alert triggered (extreme values detected)")

        st.write("**Risk Indicators:**")
        st.write(f"- Bytes Ratio: {bytes_ratio:.2f}")
        st.write(f"- Failed Logins: {failed_logins}")
        st.write(f"- Connections: {connections}")

    else:
        st.success("✅ Normal Traffic")
        st.write(f"Bytes Ratio: {bytes_ratio:.2f}")