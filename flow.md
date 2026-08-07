graph TD
    Start["1. Lệnh: python src/main.py --part 1"] --> MainPart1["2. Hàm part1_attacks() (main.py)"]
    
    MainPart1 --> CreateUnsafe["3a. create_unsafe_agent() (agents/agent.py)"]
    MainPart1 --> CreateGuards["3b. create_guards_agent() (agents/guards_agent.py)"]
    
    MainPart1 --> RunUnsafe["4. run_attacks(unsafe_agent) (attacks/attacks.py)"]
    MainPart1 --> RunGuards["5. run_attacks(guards_agent) (attacks/attacks.py)"]
    
    RunUnsafe --> LoopPrompts["6. Lấy 15 Prompts từ adversarial_prompts"]
    LoopPrompts --> ChatAgent["7. Gửi câu hỏi: chat_with_agent() (core/utils.py)"]
    ChatAgent --> Classify["8. Phân loại kết quả: classify_attack_outcome() (attacks/attacks.py)"]
    Classify --> CheckSecret["9. So khớp secret: contains_secret() (security_boundary.py)"]
    
    MainPart1 --> GenAI["10. AI tự sinh 5 prompt mới: generate_ai_attacks() (attacks/attacks.py)"]
    
    CheckSecret --> SaveJSON["11. Ghi bằng chứng: save_attack_results() (outputs/attack_results.json)"]
    GenAI --> SaveJSON
