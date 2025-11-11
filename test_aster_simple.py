#!/usr/bin/env python3
"""
Simple Aster DEX Test Script
Run from ccxt directory: uv run python test_aster_simple.py
"""
import asyncio
import sys
import os

# Add local ccxt python package to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'python'))

import ccxt.pro as ccxtpro

# 配置你的 API 凭证
API_KEY = "your_api_key_here"  # 替换为你的 API Key
SECRET = "your_secret_here"     # 替换为你的 Secret

# 或者使用环境变量
API_KEY = os.getenv('ASTER_API_KEY', API_KEY)
SECRET = os.getenv('ASTER_SECRET', SECRET)


async def test_aster():
    """测试 Aster DEX 连接"""

    print("=" * 70)
    print("🔷 Aster DEX 测试")
    print("=" * 70)

    # 初始化交易所
    exchange = ccxtpro.aster({
        'apiKey': API_KEY,
        'secret': SECRET,
        'enableRateLimit': True,
        'timeout': 30000,
        'options': {
            'defaultType': 'future',
        }
    })

    print(f"\n✅ 交易所: {exchange.name}")
    print(f"   ID: {exchange.id}")
    print(f"   是否 DEX: {exchange.dex}")
    print(f"   API URL: {exchange.urls['api']['fapiPublic']}")
    print()

    try:
        # 测试连接
        print("📡 测试连接...")
        time = await exchange.fetch_time()
        print(f"✅ 连接成功! 服务器时间: {time}")
        print()

        # 获取余额
        print("💰 获取账户余额...")
        balance = await exchange.fetch_balance()

        print("✅ 余额信息:")
        if 'total' in balance:
            for currency, amount in balance['total'].items():
                if amount > 0:
                    print(f"   {currency}: {amount}")

        # 显示详细信息
        if 'info' in balance and isinstance(balance['info'], list):
            print("\n📊 账户详情:")
            for asset in balance['info']:
                if float(asset.get('walletBalance', 0)) > 0:
                    print(f"   资产: {asset.get('asset')}")
                    print(f"   钱包余额: {asset.get('walletBalance')}")
                    print(f"   未实现盈亏: {asset.get('unrealizedProfit')}")
                    print(f"   保证金余额: {asset.get('marginBalance')}")
                    print(f"   可用余额: {asset.get('availableBalance')}")
        print()

        # 获取持仓
        print("📈 获取持仓信息...")
        positions = await exchange.fetch_positions()
        open_positions = [p for p in positions if float(p.get('contracts', 0)) != 0]

        print(f"✅ 持仓数量: {len(open_positions)}")
        if open_positions:
            for pos in open_positions:
                print(f"\n   交易对: {pos.get('symbol')}")
                print(f"   方向: {pos.get('side')}")
                print(f"   数量: {pos.get('contracts')}")
                print(f"   杠杆: {pos.get('leverage')}x")
                print(f"   未实现盈亏: {pos.get('unrealizedPnl')}")
        else:
            print("   无持仓")
        print()

        # 获取挂单
        print("📋 获取挂单...")
        orders = await exchange.fetch_open_orders()
        print(f"✅ 挂单数量: {len(orders)}")
        if orders:
            for order in orders[:5]:
                print(f"   {order['symbol']} - {order['side']} {order['type']}")
        else:
            print("   无挂单")
        print()

        print("=" * 70)
        print("✅ 测试完成!")
        print("=" * 70)

    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()

    finally:
        await exchange.close()
        print("\n🔌 连接已关闭")


if __name__ == '__main__':
    if API_KEY == "your_api_key_here" or SECRET == "your_secret_here":
        print("\n⚠️  请先设置 API 凭证!")
        print("\n方式 1: 修改脚本中的 API_KEY 和 SECRET 变量")
        print("方式 2: 设置环境变量:")
        print("  export ASTER_API_KEY='your_key'")
        print("  export ASTER_SECRET='your_secret'")
        print("  uv run python test_aster_simple.py")
        sys.exit(1)

    print("\n⚠️  警告: Aster 没有测试网，使用真实资金!")
    print("按 Ctrl+C 取消，或按 Enter 继续...")
    try:
        input()
    except KeyboardInterrupt:
        print("\n已取消")
        sys.exit(0)

    asyncio.run(test_aster())
