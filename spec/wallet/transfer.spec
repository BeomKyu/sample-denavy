# FILE: sample-denavy/spec/wallet/transfer.spec

import dna/wallet/wallet.dna (Wallet, Transaction, TxType)
import dna/user/user.dna (User)

# Input DTO defined inline with strict constraints
struct TransferReq
    sender_id: uuid
    receiver_id: uuid
    amount: u64 @min(1)
    memo: str?

# Main Logic Function
fn transfer(req: TransferReq) -> Result<Transaction, Error>
    # 1. Load Wallets
    sender <- Wallet.findById(req.sender_id) !=>! Err(WalletNotFound)
    receiver <- Wallet.findById(req.receiver_id) !=>! Err(WalletNotFound)

    # 2. Check Balance (Invariant check)
    ? sender.balance < req.amount =>! Err(InsufficientBalance)

    # 3. Execute Transfer (Atomic State Mutation)
    sender.balance <- sender.balance - req.amount
    receiver.balance <- receiver.balance + req.amount

    # 4. Persistence
    > Wallet.save(sender)
    > Wallet.save(receiver)

    # 5. Log Transaction
    tx <- Transaction(
        wallet_id: sender.id,
        counterpart_wallet_id: receiver.id,
        type: TxType.Transfer,
        amount: req.amount,
        memo: req.memo
    )
    > Transaction.save(tx)

    => Ok(tx)
