#!/usr/bin/env python3
"""Check saved native YouMind results without making any network/API call.

Usage: python3 tools/check_generation.py --expected PRIVATE.json --messages PRIVATE.json
Expected is an array of {title, text}; messages is a saved listMessages response.
Keep inputs private. Output contains counts and failure reasons, never sentences.
This checks metadata, not pronunciation or decoded media integrity.
"""
import argparse
from collections import Counter
import json
import math
from pathlib import Path


def check(expected, messages, contract):
    errors = []
    if type(contract.get('generation_speed')) not in (int, float) or contract['generation_speed'] != 1.0:
        return ['Contract must require normal generation speed 1.0.']
    titles = [item['title'] for item in expected]
    if len(titles) != len(set(titles)):
        return ['Expected titles are not unique.']
    wanted = {item['title']: item['text'] for item in expected}
    if any(not isinstance(text, str) or '[' in text or ']' in text for text in wanted.values()):
        return ['Expected sentences must be plain text without inline control tags.']
    calls = [block for message in messages.get('messages', [])
             for block in message.get('blocks', [])
             if block.get('type') == 'tool'
             and block.get('toolName') in ('generate_audio', 'generateAudio')]
    seen = Counter()
    for block in calls:
        args = block.get('toolArguments') or {}
        title = args.get('title')
        seen[title] += 1
        if title not in wanted:
            errors.append('Unexpected audio tool call.')
            continue
        # Use ordinal labels so failure output does not publish private titles/text.
        label = f'Item {titles.index(title) + 1}'
        text = wanted[title]
        required = {k: contract[k] for k in ('voice', 'language', 'mode', 'as_artifact')}
        required.update(text=text, title=title, speed=contract['generation_speed'])
        if (type(args.get('speed')) not in (int, float)
                or any(k not in args or args[k] != value for k, value in required.items())
                or set(args) - (set(required) | {'model'})
                or ('model' in args and args['model'] != contract['model'])):
            errors.append(label + ': exact arguments or explicit speed=1.0 failed.')
        if block.get('status') != 'success':
            errors.append(label + ': generation did not succeed; do not retry automatically.')
            continue
        result = block.get('toolResult') or {}
        snip = result.get('snip') or {}
        extra = snip.get('extra') or {}
        if isinstance(extra, str):
            try:
                extra = json.loads(extra)
            except ValueError:
                errors.append(label + ': invalid returned metadata.')
                continue
        if result.get('extra_info') is not None and result['extra_info'] != extra:
            errors.append(label + ': conflicting returned metadata.')
        if any(extra.get(k) != contract[k] for k in ('voice', 'model', 'language')):
            errors.append(label + ': returned voice/model/language failed.')
        if snip.get('title') != title or (snip.get('gen_config') or {}).get('content') != text:
            errors.append(label + ': returned title or configured text changed.')
        for kind in ('alignment', 'normalized_alignment'):
            alignment = extra.get(kind) or {}
            if alignment.get('characters') != list(text):
                errors.append(label + ': ' + kind + ' differs from original; tags forbidden.')
            starts = alignment.get('character_start_times_seconds')
            ends = alignment.get('character_end_times_seconds')
            if not isinstance(starts, list) or not isinstance(ends, list):
                errors.append(label + ': ' + kind + ' timing arrays missing.')
            elif (len(starts) != len(text) or len(ends) != len(text)
                    or any(type(t) not in (int, float) or not math.isfinite(t) or t < 0 for t in starts + ends)
                    or starts != sorted(starts) or ends != sorted(ends)
                    or any(end < start for start, end in zip(starts, ends))):
                errors.append(label + ': ' + kind + ' timing arrays invalid.')
        segments = extra.get('voice_segments') or []
        if (len(segments) != 1 or segments[0].get('voice_id') != contract['voice']
                or segments[0].get('character_start_index') != 0
                or segments[0].get('character_end_index') != len(text)):
            errors.append(label + ': expected one full original-text voice segment.')
        if extra.get('usage_characters') != len(text):
            errors.append(label + ': usage differs from untagged original character count.')
    if len(calls) != len(wanted) or set(seen) != set(wanted) or any(n != 1 for n in seen.values()):
        errors.append('Each expected sentence requires exactly one successful attempt; missing/duplicate calls found.')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', type=Path, required=True)
    parser.add_argument('--messages', type=Path, required=True)
    args = parser.parse_args()
    contract = json.loads((Path(__file__).resolve().parents[1] / 'generation-contract.json').read_text())
    expected = json.loads(args.expected.read_text())
    messages = json.loads(args.messages.read_text())
    errors = check(expected, messages, contract)
    print(json.dumps({'status': 'FAIL' if errors else 'PASS', 'expected_sentences': len(expected),
                      'errors': errors}, ensure_ascii=False))
    raise SystemExit(bool(errors))


if __name__ == '__main__':
    main()
